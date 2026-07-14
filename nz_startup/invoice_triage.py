"""
Invoice triage — extract fields from PDF/text invoices for accountant review.

Not OCR-as-a-service: prefers embedded text (pypdf when installed).
Never files or pays. Human verifies tax invoice validity.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

REGISTRY_FIELDS = [
    "id",
    "source_file",
    "supplier_guess",
    "invoice_number",
    "invoice_date",
    "due_date",
    "subtotal",
    "gst",
    "total",
    "currency",
    "gst_number_guess",
    "confidence",
    "flags",
    "triaged_on",
    "notes",
]

# NZ GST number often NZBN-style 9-13 digits; also "GST 123-456-789"
GST_NUM_RE = re.compile(
    r"(?:GST(?:\s*(?:No\.?|Number|#))?[:\s]*)(\d{2,3}[-\s]?\d{3}[-\s]?\d{3})",
    re.I,
)
# Require No/Number/# so plain "TAX INVOICE" header is not treated as a number line
INV_NO_RE = re.compile(
    r"(?:Tax\s*)?Invoice\s*(?:No\.?|Number|#)\s*[:.#]?\s*([A-Za-z0-9][-A-Za-z0-9/]{1,24})",
    re.I,
)
DATE_RE = re.compile(
    r"(?:Date|Invoice\s*Date|Tax\s*Date)[:\s]*(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\d{4}-\d{2}-\d{2})",
    re.I,
)
DUE_RE = re.compile(
    r"(?:Due\s*Date|Payment\s*Due)[:\s]*(\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\d{4}-\d{2}-\d{2})",
    re.I,
)
MONEY_RE = re.compile(
    r"(?:NZD|\$)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})|[0-9]+\.[0-9]{2})"
)
TOTAL_LINE_RE = re.compile(
    r"(?:^|\n)\s*(?:Invoice\s*)?Total(?:\s*\(incl(?:uding)?\.?\s*GST\))?[:\s]*\$?\s*([0-9,]+\.\d{2})",
    re.I,
)
GST_LINE_RE = re.compile(
    r"(?:^|\n)\s*(?:GST|Tax)\s*(?:@\s*15%|15%|Amount)?[:\s]*\$?\s*([0-9,]+\.\d{2})",
    re.I,
)
SUBTOTAL_RE = re.compile(
    r"(?:^|\n)\s*(?:Sub\s*-?\s*total|Net|Excl(?:uding)?\.?\s*GST)[:\s]*\$?\s*([0-9,]+\.\d{2})",
    re.I,
)
SUPPLIER_LINE_RE = re.compile(
    r"(?:From|Supplier|Bill\s*From|Sold\s*By)[:\s]*(.+)",
    re.I,
)


def finance_invoices_dir(company_id: str) -> Path:
    p = ensure_exists(company_id) / "finance" / "invoices"
    p.mkdir(parents=True, exist_ok=True)
    (p / "inbox").mkdir(exist_ok=True)
    (p / "triaged").mkdir(exist_ok=True)
    return p


def registry_path(company_id: str) -> Path:
    return finance_invoices_dir(company_id) / "invoice-registry.csv"


def extract_text(path: Path) -> tuple[str, str]:
    """
    Returns (text, method) where method is txt|pdf_pypdf|pdf_raw|empty.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".csv"}:
        return path.read_text(encoding="utf-8", errors="replace"), "txt"
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore

            reader = PdfReader(str(path))
            parts = []
            for page in reader.pages:
                parts.append(page.extract_text() or "")
            text = "\n".join(parts).strip()
            if text:
                return text, "pdf_pypdf"
        except ImportError:
            pass
        except Exception:
            pass
        # Fallback: pull readable ASCII strings from PDF binary
        raw = path.read_bytes()
        chunks = re.findall(rb"[\x20-\x7e]{4,}", raw)
        text = "\n".join(c.decode("ascii", errors="ignore") for c in chunks)
        # Heuristic cleanup
        text = re.sub(r"\n{3,}", "\n\n", text)
        if len(text) > 40:
            return text[:50000], "pdf_raw"
        return "", "empty"
    # Images: no OCR engine bundled — flag for human
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}:
        return "", "image_no_ocr"
    return path.read_text(encoding="utf-8", errors="replace"), "txt"


def _money(s: str | None) -> str:
    if not s:
        return ""
    return s.replace(",", "")


def _norm_date(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$", s)
    if not m:
        return s
    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if y < 100:
        y += 2000
    try:
        return date(y, mo, d).isoformat()
    except ValueError:
        try:
            return date(y, d, mo).isoformat()
        except ValueError:
            return s


def parse_invoice_text(text: str, source_name: str = "") -> dict[str, Any]:
    flags: list[str] = []
    conf = 0.2
    if not text or len(text.strip()) < 20:
        flags.append("little_or_no_text")
        return {
            "supplier_guess": "",
            "invoice_number": "",
            "invoice_date": "",
            "due_date": "",
            "subtotal": "",
            "gst": "",
            "total": "",
            "currency": "NZD",
            "gst_number_guess": "",
            "confidence": "low",
            "flags": flags,
            "excerpt": (text or "")[:400],
        }

    inv = INV_NO_RE.search(text)
    gstn = GST_NUM_RE.search(text)
    idate = DATE_RE.search(text)
    due = DUE_RE.search(text)
    total = TOTAL_LINE_RE.search(text)
    gst_amt = GST_LINE_RE.search(text)
    sub = SUBTOTAL_RE.search(text)
    supplier = SUPPLIER_LINE_RE.search(text)

    # Fallback supplier: first non-empty line that is not TAX INVOICE
    supplier_guess = (supplier.group(1).strip() if supplier else "")
    if not supplier_guess:
        for line in text.splitlines()[:12]:
            line = line.strip()
            if not line or re.search(r"tax\s*invoice|invoice", line, re.I):
                continue
            if len(line) > 2:
                supplier_guess = line[:80]
                break

    total_s = _money(total.group(1) if total else "")
    gst_s = _money(gst_amt.group(1) if gst_amt else "")
    sub_s = _money(sub.group(1) if sub else "")

    # Cross-check GST ≈ total * 3/23 for 15% inclusive
    if total_s and gst_s:
        try:
            t = float(total_s)
            g = float(gst_s)
            expected = round(t * 3 / 23, 2)
            if abs(expected - g) > 0.05 and abs(expected - g) > t * 0.01:
                flags.append("gst_total_mismatch_check")
            else:
                conf += 0.15
        except ValueError:
            flags.append("amount_parse_error")

    if inv:
        conf += 0.2
    if total_s:
        conf += 0.2
    if gstn:
        conf += 0.15
    if idate:
        conf += 0.1
    if "tax invoice" in text.lower():
        conf += 0.1
    else:
        flags.append("missing_tax_invoice_label")

    if conf >= 0.7:
        confidence = "high"
    elif conf >= 0.45:
        confidence = "medium"
    else:
        confidence = "low"
        flags.append("low_confidence_review_required")

    return {
        "supplier_guess": supplier_guess,
        "invoice_number": inv.group(1) if inv else "",
        "invoice_date": _norm_date(idate.group(1) if idate else ""),
        "due_date": _norm_date(due.group(1) if due else ""),
        "subtotal": sub_s,
        "gst": gst_s,
        "total": total_s,
        "currency": "NZD" if ("NZD" in text or "$" in text) else "",
        "gst_number_guess": re.sub(r"\s+", "", gstn.group(1)) if gstn else "",
        "confidence": confidence,
        "flags": flags,
        "excerpt": text[:600].replace("\r", ""),
        "source_hint": source_name,
    }


def _invoice_id(path: Path, parsed: dict[str, Any]) -> str:
    key = f"{path.name}|{parsed.get('invoice_number')}|{parsed.get('total')}|{parsed.get('invoice_date')}"
    return "I" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def _read_registry(company_id: str) -> list[dict[str, str]]:
    path = registry_path(company_id)
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_registry(company_id: str, rows: list[dict[str, str]]) -> Path:
    path = registry_path(company_id)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=REGISTRY_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in REGISTRY_FIELDS})
    _sync_registry_md(company_id, rows)
    return path


def _sync_registry_md(company_id: str, rows: list[dict[str, str]]) -> None:
    path = finance_invoices_dir(company_id) / "invoice-registry.md"
    lines = [
        "# Invoice registry (triage)",
        "",
        f"- Count: {len(rows)}",
        "- HITL: human verifies tax invoice validity before claiming GST",
        "",
        "| ID | Supplier | Inv # | Date | Total | GST | Confidence | Flags |",
        "|----|----------|-------|------|-------|-----|------------|-------|",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('id','')} | {(r.get('supplier_guess') or '')[:24]} | "
            f"{r.get('invoice_number','')} | {r.get('invoice_date','')} | "
            f"{r.get('total','')} | {r.get('gst','')} | {r.get('confidence','')} | "
            f"{(r.get('flags') or '')[:40]} |"
        )
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def triage_file(company_id: str, source: Path) -> dict[str, Any]:
    source = Path(source).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    inv_root = finance_invoices_dir(company_id)
    archived = inv_root / "inbox" / source.name
    if source.resolve() != archived.resolve():
        shutil.copy2(source, archived)

    text, method = extract_text(source)
    parsed = parse_invoice_text(text, source.name)
    if method == "image_no_ocr":
        parsed["flags"] = list(parsed.get("flags") or []) + ["image_requires_human_ocr"]
        parsed["confidence"] = "low"
    if method == "empty":
        parsed["flags"] = list(parsed.get("flags") or []) + ["extract_failed"]
        parsed["confidence"] = "low"
    if method == "pdf_raw":
        parsed["flags"] = list(parsed.get("flags") or []) + ["pdf_raw_extraction_noisy"]

    iid = _invoice_id(source, parsed)
    triaged_dir = inv_root / "triaged" / iid
    triaged_dir.mkdir(parents=True, exist_ok=True)
    # copy source into triaged
    shutil.copy2(source, triaged_dir / source.name)
    detail = {
        "id": iid,
        "extraction_method": method,
        "parsed": parsed,
        "source_file": source.name,
        "triaged_on": date.today().isoformat(),
        "hitl": "Verify before GST claim. Not a certified tax invoice review.",
    }
    (triaged_dir / "triage.json").write_text(
        json.dumps(detail, indent=2, default=str) + "\n", encoding="utf-8"
    )
    (triaged_dir / "triage.md").write_text(
        format_triage_markdown(detail), encoding="utf-8", newline="\n"
    )
    if text:
        (triaged_dir / "extracted.txt").write_text(text[:100000], encoding="utf-8")

    row = {
        "id": iid,
        "source_file": source.name,
        "supplier_guess": parsed.get("supplier_guess") or "",
        "invoice_number": parsed.get("invoice_number") or "",
        "invoice_date": parsed.get("invoice_date") or "",
        "due_date": parsed.get("due_date") or "",
        "subtotal": parsed.get("subtotal") or "",
        "gst": parsed.get("gst") or "",
        "total": parsed.get("total") or "",
        "currency": parsed.get("currency") or "",
        "gst_number_guess": parsed.get("gst_number_guess") or "",
        "confidence": parsed.get("confidence") or "low",
        "flags": ";".join(parsed.get("flags") or []),
        "triaged_on": date.today().isoformat(),
        "notes": f"method={method}",
    }
    rows = _read_registry(company_id)
    rows = [r for r in rows if r.get("id") != iid]
    rows.append(row)
    rows.sort(key=lambda r: (r.get("invoice_date") or "", r.get("id") or ""))
    _write_registry(company_id, rows)

    append_audit(
        ensure_exists(company_id),
        actor="agent:finance-clerk",
        skill="finance-clerk",
        action="invoice_triage",
        summary=f"{iid} {row['supplier_guess'][:40]} total={row['total']} conf={row['confidence']}",
        artefact_ref=f"finance/invoices/triaged/{iid}/",
        tier="gold",
        hitl_required=True,
        hitl_status="pending",
        risk_level="medium",
    )
    return detail


def triage_path(company_id: str, path: Path) -> list[dict[str, Any]]:
    """Triage a file or all files in a directory."""
    path = Path(path).expanduser().resolve()
    if path.is_file():
        return [triage_file(company_id, path)]
    if not path.is_dir():
        raise FileNotFoundError(path)
    results = []
    for f in sorted(path.iterdir()):
        if f.is_file() and f.suffix.lower() in {
            ".pdf",
            ".txt",
            ".md",
            ".png",
            ".jpg",
            ".jpeg",
        }:
            results.append(triage_file(company_id, f))
    return results


def list_invoices(company_id: str) -> list[dict[str, str]]:
    return _read_registry(company_id)


def format_triage_markdown(detail: dict[str, Any]) -> str:
    p = detail.get("parsed") or {}
    lines = [
        f"# Invoice triage — {detail.get('id')}",
        "",
        "**DRAFT triage — human verifies tax invoice before GST claim.**",
        "",
        f"- Source: {detail.get('source_file')}",
        f"- Method: {detail.get('extraction_method')}",
        f"- Confidence: {p.get('confidence')}",
        f"- Flags: {', '.join(p.get('flags') or []) or '—'}",
        "",
        "## Extracted fields",
        "",
        f"- Supplier: {p.get('supplier_guess') or '—'}",
        f"- Invoice #: {p.get('invoice_number') or '—'}",
        f"- Date: {p.get('invoice_date') or '—'}",
        f"- Due: {p.get('due_date') or '—'}",
        f"- Subtotal: {p.get('subtotal') or '—'}",
        f"- GST: {p.get('gst') or '—'}",
        f"- Total: {p.get('total') or '—'}",
        f"- GST number guess: {p.get('gst_number_guess') or '—'}",
        "",
        "## Excerpt",
        "",
        "```",
        (p.get("excerpt") or "")[:800],
        "```",
        "",
        f"HITL: {detail.get('hitl')}",
        "",
    ]
    return "\n".join(lines)


def format_registry_summary(company_id: str) -> str:
    rows = list_invoices(company_id)
    lines = [
        "# Invoice triage summary",
        "",
        f"- Registered: {len(rows)}",
        f"- Low confidence: {sum(1 for r in rows if r.get('confidence') == 'low')}",
        "",
    ]
    for r in rows:
        lines.append(
            f"- `{r.get('id')}` **{r.get('supplier_guess') or '?'}** "
            f"#{r.get('invoice_number') or '—'} total={r.get('total') or '—'} "
            f"[{r.get('confidence')}]"
        )
    lines.append("")
    lines.append("Human verifies before claiming GST.")
    return "\n".join(lines)
