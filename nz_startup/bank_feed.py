"""
Bank feed CSV import and bookkeeping triage (read-only assist).

Never moves money. Never talks to the bank API — human exports CSV.
"""
from __future__ import annotations

import csv
import hashlib
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists
from nz_startup.untrusted import strip_injection_flags

NORMALIZED_FIELDS = [
    "id",
    "date",
    "description",
    "amount",
    "direction",  # inflow | outflow
    "balance",
    "category_guess",
    "gst_hint",  # likely_taxable | likely_exempt_or_personal | unknown
    "notes",
    "source_file",
    "import_batch",
]

# Flexible header aliases (lowercase)
DATE_ALIASES = {"date", "transaction date", "posted", "value date", "tran date"}
DESC_ALIASES = {
    "description",
    "narrative",
    "details",
    "memo",
    "particulars",
    "payee",
    "transaction description",
}
AMOUNT_ALIASES = {"amount", "transaction amount", "value", "nzd", "sum"}
DEBIT_ALIASES = {"debit", "withdrawal", "money out", "out"}
CREDIT_ALIASES = {"credit", "deposit", "money in", "in"}
BALANCE_ALIASES = {"balance", "running balance", "account balance"}

CATEGORY_RULES: list[tuple[re.Pattern[str], str, str]] = [
    (re.compile(r"\b(xero|ird|inland revenue|gst)\b", re.I), "tax_authority", "likely_taxable"),
    (re.compile(r"\b(salary|wages|payrun|payroll)\b", re.I), "payroll", "likely_exempt_or_personal"),
    (re.compile(r"\b(interest|dividend)\b", re.I), "finance_income", "unknown"),
    (re.compile(r"\b(aws|azure|google cloud|github|openai|anthropic|digitalocean)\b", re.I), "software_saas", "likely_taxable"),
    (re.compile(r"\b(spark|one nz|2degrees|vodafone|skinning)\b", re.I), "telecom", "likely_taxable"),
    (re.compile(r"\b(bp|z energy|mobil|caltex|petrol|fuel)\b", re.I), "vehicle_fuel", "likely_taxable"),
    (re.compile(r"\b(uber|taxi|parking)\b", re.I), "travel", "likely_taxable"),
    (re.compile(r"\b(countdown|new world|pak.?n.?save|warehouse)\b", re.I), "personal_or_supplies", "unknown"),
    (re.compile(r"\b(transfer|to myself|savings)\b", re.I), "transfer", "likely_exempt_or_personal"),
    (re.compile(r"\b(invoice|customer|payment received|stripe|paypal)\b", re.I), "sales_receipt", "likely_taxable"),
    (re.compile(r"\b(rent|lease)\b", re.I), "premises", "likely_taxable"),
    (re.compile(r"\b(insurance)\b", re.I), "insurance", "likely_taxable"),
]


def finance_dir(company_id: str) -> Path:
    p = ensure_exists(company_id) / "finance"
    p.mkdir(parents=True, exist_ok=True)
    return p


def bank_csv_path(company_id: str) -> Path:
    return finance_dir(company_id) / "bank-feed.csv"


def imports_dir(company_id: str) -> Path:
    p = finance_dir(company_id) / "bank-imports"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _norm_header(h: str) -> str:
    return re.sub(r"\s+", " ", (h or "").strip().lower())


def _pick(headers: list[str], aliases: set[str]) -> str | None:
    for h in headers:
        if _norm_header(h) in aliases:
            return h
    return None


def _parse_amount(raw: str) -> float | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s in ("-", "—"):
        return None
    s = s.replace(",", "").replace("$", "").replace("NZD", "").strip()
    # accounting negatives (1,234.56)
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return ""
    # already ISO
    if re.match(r"^\d{4}-\d{2}-\d{2}", s):
        return s[:10]
    # DD/MM/YYYY or D/M/YYYY (NZ common)
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$", s)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y < 100:
            y += 2000
        try:
            return date(y, mo, d).isoformat()
        except ValueError:
            # try US-style swap if invalid
            try:
                return date(y, d, mo).isoformat()
            except ValueError:
                return s
    return s


def _categorize(description: str, amount: float) -> tuple[str, str]:
    for pattern, cat, gst in CATEGORY_RULES:
        if pattern.search(description or ""):
            return cat, gst
    if amount > 0:
        return "uncategorised_inflow", "unknown"
    return "uncategorised_outflow", "unknown"


def _row_id(date_s: str, desc: str, amount: float, idx: int) -> str:
    base = f"{date_s}|{desc}|{amount:.2f}|{idx}"
    return "B" + hashlib.sha1(base.encode("utf-8")).hexdigest()[:10]


def detect_mapping(headers: list[str]) -> dict[str, str | None]:
    return {
        "date": _pick(headers, DATE_ALIASES),
        "description": _pick(headers, DESC_ALIASES),
        "amount": _pick(headers, AMOUNT_ALIASES),
        "debit": _pick(headers, DEBIT_ALIASES),
        "credit": _pick(headers, CREDIT_ALIASES),
        "balance": _pick(headers, BALANCE_ALIASES),
    }


def parse_bank_csv(path: Path) -> tuple[list[dict[str, str]], dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    # skip empty leading lines
    lines = text.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip():
            start = i
            break
    sample = "\n".join(lines[start : start + 5])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(lines[start:], dialect=dialect)
    if not reader.fieldnames:
        raise ValueError("CSV has no header row")
    headers = list(reader.fieldnames)
    mapping = detect_mapping(headers)
    if not mapping["date"] or not mapping["description"]:
        raise ValueError(
            f"Could not detect date/description columns. Headers: {headers}. "
            "Rename columns to Date, Description, Amount (or Debit/Credit)."
        )
    if not mapping["amount"] and not (mapping["debit"] or mapping["credit"]):
        raise ValueError(
            "Could not detect Amount or Debit/Credit columns. "
            f"Headers: {headers}"
        )

    rows: list[dict[str, str]] = []
    for idx, raw in enumerate(reader):
        date_s = _parse_date(raw.get(mapping["date"] or "", ""))
        desc_raw = (raw.get(mapping["description"] or "") or "").strip()
        # G2 — flag injection-like bank narratives; keep structured CSV clean
        desc, inj_flags = strip_injection_flags(desc_raw)
        if not date_s and not desc:
            continue
        amount: float | None = None
        if mapping["amount"]:
            amount = _parse_amount(raw.get(mapping["amount"] or "", ""))
        else:
            debit = _parse_amount(raw.get(mapping["debit"] or "", "") or "0") or 0.0
            credit = _parse_amount(raw.get(mapping["credit"] or "", "") or "0") or 0.0
            # NZ bank exports: credit = money in (positive), debit = money out
            amount = credit - debit
        if amount is None:
            continue
        balance_raw = raw.get(mapping["balance"] or "", "") if mapping["balance"] else ""
        balance = _parse_amount(balance_raw) if balance_raw else None
        cat, gst = _categorize(desc, amount)
        direction = "inflow" if amount >= 0 else "outflow"
        notes = ""
        if inj_flags:
            notes = f"untrusted_flags:{','.join(inj_flags)}"
        rows.append(
            {
                "id": _row_id(date_s, desc, amount, idx),
                "date": date_s,
                "description": desc,
                "amount": f"{amount:.2f}",
                "direction": direction,
                "balance": f"{balance:.2f}" if balance is not None else "",
                "category_guess": cat,
                "gst_hint": gst,
                "notes": notes,
                "source_file": path.name,
                "import_batch": "",
            }
        )
    meta = {
        "headers": headers,
        "mapping": mapping,
        "row_count": len(rows),
        "source": str(path),
    }
    return rows, meta


def _read_existing(company_id: str) -> list[dict[str, str]]:
    path = bank_csv_path(company_id)
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_rows(company_id: str, rows: list[dict[str, str]]) -> Path:
    path = bank_csv_path(company_id)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=NORMALIZED_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in NORMALIZED_FIELDS})
    _sync_markdown(company_id, rows)
    return path


def _sync_markdown(company_id: str, rows: list[dict[str, str]]) -> None:
    path = finance_dir(company_id) / "bank-feed.md"
    lines = [
        "# Bank feed (imported)",
        "",
        f"- Rows: {len(rows)}",
        "- Source of truth: `bank-feed.csv`",
        "- HITL: triage only — never moves money",
        "",
        "| Date | Description | Amount | Direction | Category guess | GST hint |",
        "|------|-------------|--------|-----------|----------------|----------|",
    ]
    for r in rows[-50:]:  # last 50 for readability
        desc = (r.get("description") or "").replace("|", "/")[:40]
        lines.append(
            f"| {r.get('date','')} | {desc} | {r.get('amount','')} | "
            f"{r.get('direction','')} | {r.get('category_guess','')} | {r.get('gst_hint','')} |"
        )
    if len(rows) > 50:
        lines.append("")
        lines.append(f"_Showing last 50 of {len(rows)} rows._")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def import_csv(
    company_id: str,
    source: Path,
    *,
    replace: bool = False,
    batch_label: str | None = None,
) -> dict[str, Any]:
    source = Path(source).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)

    # Archive original
    batch = batch_label or date.today().isoformat()
    archived = imports_dir(company_id) / f"{batch}-{source.name}"
    shutil.copy2(source, archived)

    new_rows, meta = parse_bank_csv(source)
    for r in new_rows:
        r["import_batch"] = batch
        r["source_file"] = source.name

    existing = [] if replace else _read_existing(company_id)
    existing_ids = {r.get("id") for r in existing}
    added = 0
    skipped = 0
    for r in new_rows:
        if r["id"] in existing_ids:
            skipped += 1
            continue
        existing.append(r)
        existing_ids.add(r["id"])
        added += 1

    # Sort by date then description
    existing.sort(key=lambda r: (r.get("date") or "", r.get("description") or ""))
    out_path = _write_rows(company_id, existing)

    summary = {
        "company_id": company_id,
        "source": str(source),
        "archived": str(archived),
        "batch": batch,
        "parsed": len(new_rows),
        "added": added,
        "skipped_duplicates": skipped,
        "total_rows": len(existing),
        "mapping": meta["mapping"],
        "output": str(out_path),
        "hitl": "Triage suggestions only. Human reconciles in Xero/myIR.",
    }
    flagged = sum(1 for r in new_rows if "untrusted_flags" in (r.get("notes") or ""))
    summary["untrusted_flagged_rows"] = flagged
    append_audit(
        ensure_exists(company_id),
        actor="agent:finance-clerk",
        skill="finance-clerk",
        action="bank_feed_import",
        summary=f"Imported {added} rows from {source.name} (skipped {skipped}; untrusted_flags={flagged})",
        artefact_ref="finance/bank-feed.csv",
        tier="gold",
        risk_level="medium",
        model_tier="light",
        outcome="ok",
    )
    return summary


def list_transactions(
    company_id: str,
    *,
    direction: str | None = None,
    category: str | None = None,
    limit: int = 100,
) -> list[dict[str, str]]:
    rows = _read_existing(company_id)
    if direction:
        d = direction.lower().strip()
        rows = [r for r in rows if (r.get("direction") or "").lower() == d]
    if category:
        c = category.lower().strip()
        rows = [r for r in rows if (r.get("category_guess") or "").lower() == c]
    return rows[-limit:]


def triage_summary(company_id: str) -> dict[str, Any]:
    rows = _read_existing(company_id)
    by_cat: dict[str, int] = {}
    by_gst: dict[str, int] = {}
    inflow = 0.0
    outflow = 0.0
    for r in rows:
        cat = r.get("category_guess") or "unknown"
        by_cat[cat] = by_cat.get(cat, 0) + 1
        g = r.get("gst_hint") or "unknown"
        by_gst[g] = by_gst.get(g, 0) + 1
        try:
            amt = float(r.get("amount") or 0)
        except ValueError:
            amt = 0.0
        if amt >= 0:
            inflow += amt
        else:
            outflow += abs(amt)
    return {
        "total_rows": len(rows),
        "inflow_sum": round(inflow, 2),
        "outflow_sum": round(outflow, 2),
        "net": round(inflow - outflow, 2),
        "by_category": dict(sorted(by_cat.items(), key=lambda x: -x[1])),
        "by_gst_hint": by_gst,
        "uncategorised": by_cat.get("uncategorised_inflow", 0)
        + by_cat.get("uncategorised_outflow", 0),
    }


def format_triage_markdown(company_id: str) -> str:
    s = triage_summary(company_id)
    lines = [
        "# Bank feed triage",
        "",
        f"- Rows: {s['total_rows']}",
        f"- Inflow: {s['inflow_sum']}",
        f"- Outflow: {s['outflow_sum']}",
        f"- Net: {s['net']}",
        f"- Uncategorised: {s['uncategorised']}",
        "",
        "## By category guess",
        "",
    ]
    for k, v in (s.get("by_category") or {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.extend(["", "## GST hints", ""])
    for k, v in (s.get("by_gst_hint") or {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.extend(
        [
            "",
            "NOT A TAX FILING — human or accountant verifies categories and GST treatment.",
            "Agent does not move money or file with IRD.",
            "",
        ]
    )
    return "\n".join(lines)
