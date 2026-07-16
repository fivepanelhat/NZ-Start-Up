"""Company status dashboard - readiness scores without sending/filing."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup import (
 __version__,
 bank_feed,
 calendar_ops,
 grants,
 invoice_triage,
 pipeline,
 rdti,
)
from nz_startup.memory import ensure_exists
from nz_startup.paths import company_dir


def _exists(company_id: str, rel: str) -> bool:
 return (company_dir(company_id) / rel).is_file()


def _dir_nonempty(company_id: str, rel: str) -> bool:
 p = company_dir(company_id) / rel
 return p.is_dir() and any(p.iterdir())


def collect_status(company_id: str) -> dict[str, Any]:
 ensure_exists(company_id)
 checks: list[dict[str, Any]] = []

 def add(area: str, ok: bool, detail: str, weight: int = 1) -> None:
 checks.append({"area": area, "ok": ok, "detail": detail, "weight": weight})

 # Profile / memory
 add("profile", _exists(company_id, "profile.md"), "profile.md present")
 add("decisions", _exists(company_id, "decisions.md"), "decisions.md present")

 # Pipeline
 deals = pipeline.list_deals(company_id)
 active = [d for d in deals if d.get("stage") not in ("won", "lost")]
 add("pipeline", len(deals) > 0, f"{len(deals)} deals ({len(active)} active)", 2)

 # Calendar
 try:
 rem = calendar_ops.reminders(company_id, within_days=14)
 actionable = rem.get("count_actionable", 0)
 overdue = len(rem.get("overdue") or [])
 add(
 "calendar",
 True,
 f"{actionable} actionable in 14d | {overdue} overdue",
 2,
 )
 except Exception as e: # noqa: BLE001
 add("calendar", False, f"error: {e}", 2)

 # RDTI
 rdti_rows = rdti.list_entries(company_id, limit=500)
 add("rdti_log", len(rdti_rows) > 0, f"{len(rdti_rows)} activity rows", 2)

 # Grants
 g_rows = grants.list_grants(company_id)
 add("grants", len(g_rows) > 0, f"{len(g_rows)} opportunities tracked")

 # Finance
 bank_rows = bank_feed.list_transactions(company_id, limit=100000)
 add("bank_feed", len(bank_rows) > 0, f"{len(bank_rows)} bank rows", 2)
 add("xero_snapshot", _exists(company_id, "finance/xero-snapshot.md"), "xero-snapshot.md")
 add(
 "gst_papers",
 _exists(company_id, "finance/gst/gst-worksheet-latest.md"),
 "gst-worksheet-latest.md",
 2,
 )
 inv = invoice_triage.list_invoices(company_id)
 add("invoices", len(inv) > 0, f"{len(inv)} triaged invoices")

 # Cadence / packs
 weekly_dir = company_dir(company_id) / "weekly"
 weekly_count = len(list(weekly_dir.glob("*.md"))) if weekly_dir.is_dir() else 0
 add("weekly_board", weekly_count > 0, f"{weekly_count} weekly report(s)", 2)
 add(
 "handoff_pack",
 _exists(company_id, "handoff/handoff-latest.zip"),
 "handoff-latest.zip",
 )
 add(
 "deadline_exports",
 _exists(company_id, "exports/deadlines-latest.ics"),
 "deadlines-latest.ics",
 )

 scored = sum(c["weight"] for c in checks if c["ok"])
 total_w = sum(c["weight"] for c in checks) or 1
 score = round(100 * scored / total_w)

 if score >= 80:
 band = "ready"
 elif score >= 50:
 band = "progressing"
 else:
 band = "early"

 gaps = [c for c in checks if not c["ok"]]
 next_actions = []
 area_to_action = {
 "profile": "Edit profile.md with non-secret company facts",
 "pipeline": "nz-startup pipeline add <id> --account ... --stage discovery",
 "calendar": "nz-startup calendar add ... or calendar seed",
 "rdti_log": "nz-startup rdti add ... (never invent hours)",
 "grants": "nz-startup grants seed <id>",
 "bank_feed": "nz-startup bank import <id> --file ...",
 "xero_snapshot": "nz-startup xero snapshot <id> [--offline]",
 "gst_papers": "nz-startup gst prepare <id> --start ... --end ...",
 "invoices": "nz-startup invoice triage <id> --path ...",
 "weekly_board": "nz-startup weekly <id>",
 "handoff_pack": "nz-startup handoff pack <id>",
 "deadline_exports": "nz-startup export reminders <id>",
 }
 for g in gaps:
 act = area_to_action.get(g["area"])
 if act:
 next_actions.append(act)

 return {
 "company_id": company_id,
 "product_version": __version__,
 "as_of": date.today().isoformat(),
 "score": score,
 "band": band,
 "checks": checks,
 "gaps": [{"area": g["area"], "detail": g["detail"]} for g in gaps],
 "next_actions": next_actions[:8],
 "hitl": (
 "Status is informational. Agents still must not file, send, or pay."
 ),
 "snapshot": {
 "pipeline_deals": len(deals),
 "pipeline_active": len(active),
 "rdti_rows": len(rdti_rows),
 "grants": len(g_rows),
 "bank_rows": len(bank_rows),
 "invoices": len(inv),
 "weekly_reports": weekly_count,
 },
 }


def format_status_markdown(status: dict[str, Any]) -> str:
 lines = [
 f"# Company status - `{status.get('company_id')}`",
 "",
 f"- Score: **{status.get('score')}/100** ({status.get('band')})",
 f"- As of: {status.get('as_of')}",
 f"- Product: v{status.get('product_version')}",
 "",
 status.get("hitl", ""),
 "",
 "## Snapshot",
 "",
 ]
 snap = status.get("snapshot") or {}
 for k, v in snap.items():
 lines.append(f"- {k.replace('_', ' ')}: {v}")
 lines.extend(["", "## Checks", ""])
 for c in status.get("checks") or []:
 mark = "OK" if c.get("ok") else "GAP"
 lines.append(f"- [{mark}] **{c.get('area')}** - {c.get('detail')}")
 lines.extend(["", "## Next actions", ""])
 actions = status.get("next_actions") or []
 if not actions:
 lines.append("_No critical gaps - run weekly board and keep RDTI contemporaneous._")
 for a in actions:
 lines.append(f"- [ ] `{a}`")
 lines.append("")
 return "\n".join(lines)


def write_status(company_id: str) -> tuple[dict[str, Any], Path]:
 status = collect_status(company_id)
 company = company_dir(company_id)
 out = company / "status"
 out.mkdir(exist_ok=True)
 md = out / "status-latest.md"
 js = out / "status-latest.json"
 md.write_text(format_status_markdown(status), encoding="utf-8", newline="\n")
 js.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
 return status, md
