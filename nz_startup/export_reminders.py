"""Export calendar reminders to ICS and markdown digests."""
from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from nz_startup import calendar_ops
from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists


def _ics_escape(text: str) -> str:
    return (
        (text or "")
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _uid(company_id: str, item_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9-]", "", f"{company_id}-{item_id}")
    return f"{safe}@nz-startup-in-a-box.local"


def _parse_due(due: str) -> date | None:
    due = (due or "").strip()
    if not due or due.upper() in ("TBD", "WEEKLY", "ONGOING", "N/A"):
        return None
    try:
        return date.fromisoformat(due[:10])
    except ValueError:
        return None


def build_ics(
    company_id: str,
    *,
    within_days: int = 90,
    include_overdue: bool = True,
    calendar_name: str | None = None,
) -> str:
    data = calendar_ops.reminders(
        company_id, within_days=within_days, include_overdue=include_overdue
    )
    events: list[dict[str, Any]] = list(data.get("overdue") or []) + list(
        data.get("upcoming") or []
    )
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cal_name = calendar_name or f"NZ Start-Up — {company_id}"
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Coastal Alpine Tech//NZ Start-Up in a Box//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{_ics_escape(cal_name)}",
    ]
    for r in events:
        d = _parse_due(r.get("due", ""))
        if not d:
            continue
        # All-day event: DTEND is exclusive next day
        dt_start = d.strftime("%Y%m%d")
        dt_end = (d + timedelta(days=1)).strftime("%Y%m%d")
        summary = r.get("item") or "Deadline"
        desc = (
            f"Owner: {r.get('owner')}\\n"
            f"Status: {r.get('status')}\\n"
            f"Category: {r.get('category')}\\n"
            f"ID: {r.get('id')}\\n"
            "INFORMATION ONLY — not a compliance certificate. Human files."
        )
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{_uid(company_id, r.get('id') or summary)}",
                f"DTSTAMP:{now}",
                f"DTSTART;VALUE=DATE:{dt_start}",
                f"DTEND;VALUE=DATE:{dt_end}",
                f"SUMMARY:{_ics_escape(summary)}",
                f"DESCRIPTION:{_ics_escape(desc)}",
                "STATUS:CONFIRMED",
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def build_digest(
    company_id: str,
    *,
    within_days: int = 14,
) -> str:
    """Markdown digest suitable for email paste or board pack."""
    body = calendar_ops.format_reminders_markdown(company_id, within_days=within_days)
    header = (
        f"# Founder deadline digest — {company_id}\n\n"
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n\n"
        "Export only. Agent does not send this digest by email.\n\n"
    )
    return header + body + "\n"


def export_all(
    company_id: str,
    *,
    within_days: int = 14,
    ics_days: int = 90,
) -> dict[str, Path]:
    company = ensure_exists(company_id)
    out_dir = company / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()

    ics_text = build_ics(company_id, within_days=ics_days)
    digest_text = build_digest(company_id, within_days=within_days)

    ics_path = out_dir / f"deadlines-{stamp}.ics"
    digest_path = out_dir / f"deadline-digest-{stamp}.md"
    latest_ics = out_dir / "deadlines-latest.ics"
    latest_digest = out_dir / "deadline-digest-latest.md"

    ics_path.write_text(ics_text, encoding="utf-8", newline="\n")
    digest_path.write_text(digest_text, encoding="utf-8", newline="\n")
    latest_ics.write_text(ics_text, encoding="utf-8", newline="\n")
    latest_digest.write_text(digest_text, encoding="utf-8", newline="\n")

    append_audit(
        company,
        actor="agent:compliance-registrar",
        skill="compliance-registrar",
        action="export_reminders",
        summary=f"Exported ICS + digest (window {within_days}d / ics {ics_days}d)",
        artefact_ref="exports/",
        tier="diamond",
    )
    return {
        "ics": ics_path,
        "digest": digest_path,
        "ics_latest": latest_ics,
        "digest_latest": latest_digest,
    }
