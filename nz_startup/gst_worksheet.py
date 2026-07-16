"""
GST worksheet assist - prepares working papers from bank feed + Xero snapshot.

NOT a tax filing. Human or accountant files in myIR.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup import bank_feed
from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists
from nz_startup.paths import templates_dir

# NZ standard rate - educational default; human confirms applicability
DEFAULT_GST_RATE = 0.15


def _parse_iso(d: str) -> date | None:
 try:
 return date.fromisoformat((d or "")[:10])
 except ValueError:
 return None


def _in_period(d: str, start: date, end: date) -> bool:
 parsed = _parse_iso(d)
 if not parsed:
 return False
 return start <= parsed <= end


def _load_xero(company_id: str) -> dict[str, Any] | None:
 path = ensure_exists(company_id) / "finance" / "xero-snapshot.json"
 if not path.is_file():
 return None
 try:
 return json.loads(path.read_text(encoding="utf-8"))
 except json.JSONDecodeError:
 return None


def _bank_rows_in_period(
 company_id: str, start: date, end: date
) -> list[dict[str, str]]:
 rows = bank_feed.list_transactions(company_id, limit=100000)
 return [r for r in rows if _in_period(r.get("date") or "", start, end)]


def build_worksheet(
 company_id: str,
 *,
 period_start: str,
 period_end: str,
 gst_rate: float = DEFAULT_GST_RATE,
 label: str | None = None,
) -> dict[str, Any]:
 start = _parse_iso(period_start)
 end = _parse_iso(period_end)
 if not start or not end:
 raise ValueError("period_start and period_end must be ISO dates YYYY-MM-DD")
 if end < start:
 raise ValueError("period_end must be on or after period_start")
 if gst_rate < 0 or gst_rate > 1:
 raise ValueError("gst_rate must be between 0 and 1 (e.g. 0.15)")

 bank_rows = _bank_rows_in_period(company_id, start, end)
 xero = _load_xero(company_id)

 sales_inflows = []
 purchases_outflows = []
 transfers = []
 unknown = []

 for r in bank_rows:
 try:
 amt = float(r.get("amount") or 0)
 except ValueError:
 amt = 0.0
 cat = r.get("category_guess") or ""
 hint = r.get("gst_hint") or "unknown"
 entry = {
 "date": r.get("date"),
 "description": r.get("description"),
 "amount": round(amt, 2),
 "category_guess": cat,
 "gst_hint": hint,
 }
 if cat == "transfer":
 transfers.append(entry)
 elif amt >= 0:
 if hint == "likely_taxable" or cat == "sales_receipt":
 sales_inflows.append(entry)
 else:
 unknown.append(entry)
 else:
 if hint == "likely_taxable":
 purchases_outflows.append(entry)
 elif hint == "likely_exempt_or_personal":
 transfers.append(entry) # treat as non-claimable bucket for review
 else:
 unknown.append(entry)

 sales_total = round(sum(e["amount"] for e in sales_inflows), 2)
 purchases_total = round(sum(abs(e["amount"]) for e in purchases_outflows), 2)

 # GST extraction assuming amounts are GST-inclusive (common for bank feeds)
 def gst_from_inclusive(total: float, rate: float) -> float:
 return round(total * rate / (1 + rate), 2)

 gst_on_sales = gst_from_inclusive(sales_total, gst_rate) if sales_total else 0.0
 gst_on_purchases = (
 gst_from_inclusive(purchases_total, gst_rate) if purchases_total else 0.0
 )
 net_gst = round(gst_on_sales - gst_on_purchases, 2)

 xero_inv = (xero or {}).get("invoices_summary") or {}
 worksheet = {
 "status": "DRAFT_WORKING_PAPERS",
 "not_a_tax_filing": True,
 "company_id": company_id,
 "period_start": start.isoformat(),
 "period_end": end.isoformat(),
 "label": label or f"GST {start.isoformat()} to {end.isoformat()}",
 "assumptions": [
 f"Default GST rate {gst_rate:.0%} - confirm if zero-rated/exempt supplies apply",
 "Bank amounts treated as GST-inclusive for estimate only",
 "Category guesses are heuristic - human must verify tax invoices",
 "Transfers and personal items excluded from claimable estimates where tagged",
 ],
 "bank": {
 "rows_in_period": len(bank_rows),
 "sales_like_inflows": sales_inflows,
 "purchase_like_outflows": purchases_outflows,
 "excluded_or_transfer": transfers,
 "needs_review": unknown,
 "sales_total_incl_est": sales_total,
 "purchases_total_incl_est": purchases_total,
 },
 "gst_estimate": {
 "rate": gst_rate,
 "gst_on_sales_est": gst_on_sales,
 "gst_on_purchases_est": gst_on_purchases,
 "net_gst_est": net_gst,
 "direction": "payable" if net_gst >= 0 else "refund_or_credit",
 },
 "xero": {
 "snapshot_mode": (xero or {}).get("mode"),
 "org_name": ((xero or {}).get("organisation") or {}).get("Name"),
 "authorised_invoices_count": xero_inv.get("count"),
 "authorised_invoices_total_approx": xero_inv.get("authorised_total_approx"),
 "note": "Xero totals may not match bank period - reconciling is human work",
 },
 "human_checklist": _checklist_items(),
 "hitl": "Human or accountant files in myIR. Agent does not file or pay.",
 }
 return worksheet


def _checklist_items() -> list[str]:
 template = templates_dir() / "gst-prep-checklist.md"
 items = [
 "Confirm GST registration and filing frequency",
 "Confirm period start/end matches IRD portal",
 "Verify sales invoices and whether amounts are GST-inclusive",
 "Verify purchase tax invoices on hand (required for claims)",
 "Review needs_review and transfer buckets",
 "Reconcile bank totals to Xero / cashbook",
 "Human or accountant files return in myIR",
 "Do not treat agent estimate as filed liability",
 ]
 if template.is_file():
 for line in template.read_text(encoding="utf-8").splitlines():
 if line.strip().startswith("- ["):
 items.append(line.strip().lstrip("- [ ]").strip())
 return items


def write_worksheet(company_id: str, worksheet: dict[str, Any]) -> dict[str, Path]:
 company = ensure_exists(company_id)
 finance = company / "finance" / "gst"
 finance.mkdir(parents=True, exist_ok=True)
 start = worksheet["period_start"]
 end = worksheet["period_end"]
 stem = f"gst-worksheet-{start}_to_{end}"

 json_path = finance / f"{stem}.json"
 md_path = finance / f"{stem}.md"
 csv_path = finance / f"{stem}-lines.csv"
 latest_md = finance / "gst-worksheet-latest.md"
 latest_json = finance / "gst-worksheet-latest.json"

 json_path.write_text(
 json.dumps(worksheet, indent=2, default=str) + "\n", encoding="utf-8"
 )
 md = format_worksheet_markdown(worksheet)
 md_path.write_text(md, encoding="utf-8", newline="\n")
 latest_md.write_text(md, encoding="utf-8", newline="\n")
 latest_json.write_text(
 json.dumps(worksheet, indent=2, default=str) + "\n", encoding="utf-8"
 )

 # Line detail CSV for accountant
 with csv_path.open("w", encoding="utf-8", newline="") as f:
 w = csv.DictWriter(
 f,
 fieldnames=[
 "bucket",
 "date",
 "description",
 "amount",
 "category_guess",
 "gst_hint",
 ],
 )
 w.writeheader()
 bank = worksheet.get("bank") or {}
 for bucket, key in (
 ("sales_like", "sales_like_inflows"),
 ("purchase_like", "purchase_like_outflows"),
 ("excluded_or_transfer", "excluded_or_transfer"),
 ("needs_review", "needs_review"),
 ):
 for e in bank.get(key) or []:
 w.writerow(
 {
 "bucket": bucket,
 "date": e.get("date"),
 "description": e.get("description"),
 "amount": e.get("amount"),
 "category_guess": e.get("category_guess"),
 "gst_hint": e.get("gst_hint"),
 }
 )

 append_audit(
 company,
 actor="agent:finance-clerk",
 skill="finance-clerk",
 action="gst_worksheet_prepare",
 summary=f"GST working papers {start}->{end} net_est={worksheet['gst_estimate']['net_gst_est']}",
 artefact_ref=f"finance/gst/{stem}.md",
 tier="gold",
 hitl_required=True,
 hitl_status="pending",
 risk_level="high",
 )
 return {
 "json": json_path,
 "markdown": md_path,
 "lines_csv": csv_path,
 "latest_md": latest_md,
 "latest_json": latest_json,
 }


def format_worksheet_markdown(ws: dict[str, Any]) -> str:
 est = ws.get("gst_estimate") or {}
 bank = ws.get("bank") or {}
 xero = ws.get("xero") or {}
 lines = [
 f"# GST working papers - {ws.get('label')}",
 "",
 "**NOT A TAX FILING** - DRAFT working papers only.",
 f"**HITL:** {ws.get('hitl')}",
 "",
 "## Period",
 "",
 f"- Start: {ws.get('period_start')}",
 f"- End: {ws.get('period_end')}",
 f"- Company: {ws.get('company_id')}",
 "",
 "## Assumptions",
 "",
 ]
 for a in ws.get("assumptions") or []:
 lines.append(f"- {a}")
 lines.extend(
 [
 "",
 "## Estimate (GST-inclusive bank heuristic)",
 "",
 f"- Rate: {est.get('rate')}",
 f"- Sales-like total (incl): {bank.get('sales_total_incl_est')}",
 f"- Purchase-like total (incl): {bank.get('purchases_total_incl_est')}",
 f"- GST on sales (est): {est.get('gst_on_sales_est')}",
 f"- GST on purchases (est): {est.get('gst_on_purchases_est')}",
 f"- **Net GST (est): {est.get('net_gst_est')}** ({est.get('direction')})",
 "",
 "## Bank coverage",
 "",
 f"- Rows in period: {bank.get('rows_in_period')}",
 f"- Sales-like lines: {len(bank.get('sales_like_inflows') or [])}",
 f"- Purchase-like lines: {len(bank.get('purchase_like_outflows') or [])}",
 f"- Excluded/transfer: {len(bank.get('excluded_or_transfer') or [])}",
 f"- Needs review: {len(bank.get('needs_review') or [])}",
 "",
 "## Xero snapshot (if present)",
 "",
 f"- Mode: {xero.get('snapshot_mode')}",
 f"- Org: {xero.get('org_name')}",
 f"- Authorised invoices count: {xero.get('authorised_invoices_count')}",
 f"- Authorised invoices total approx: {xero.get('authorised_invoices_total_approx')}",
 f"- Note: {xero.get('note')}",
 "",
 "## Needs human review (sample)",
 "",
 ]
 )
 for e in (bank.get("needs_review") or [])[:15]:
 lines.append(
 f"- {e.get('date')} | {e.get('description')} | {e.get('amount')} | "
 f"{e.get('category_guess')} / {e.get('gst_hint')}"
 )
 if not (bank.get("needs_review") or []):
 lines.append("_None tagged needs_review_")
 lines.extend(["", "## Human checklist", ""])
 for c in ws.get("human_checklist") or []:
 lines.append(f"- [ ] {c}")
 lines.extend(
 [
 "",
 "---",
 "Prepared by finance-clerk assist. Confirm with accountant before myIR.",
 "",
 ]
 )
 return "\n".join(lines)


def prepare_and_write(
 company_id: str,
 *,
 period_start: str,
 period_end: str,
 gst_rate: float = DEFAULT_GST_RATE,
 label: str | None = None,
) -> tuple[dict[str, Any], dict[str, Path]]:
 ws = build_worksheet(
 company_id,
 period_start=period_start,
 period_end=period_end,
 gst_rate=gst_rate,
 label=label,
 )
 paths = write_worksheet(company_id, ws)
 return ws, paths
