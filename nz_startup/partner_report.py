"""
Cohort partner report — anonymised or named seat readiness for EDAs.

Local markdown/JSON only. Does not email partners.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup import cohort, status
from nz_startup.cohort import cohorts_root
from nz_startup.paths import company_dir


def build_partner_report(
    cohort_id: str,
    *,
    anonymise: bool = False,
) -> dict[str, Any]:
    cfg = cohort.load_config(cohort_id)
    seats = cfg.get("seats") or []
    seat_rows: list[dict[str, Any]] = []
    scores: list[int] = []

    for i, seat in enumerate(seats, start=1):
        cid = seat.get("company_id") or ""
        label = f"seat-{i:02d}" if anonymise else seat.get("founder_id") or cid
        row: dict[str, Any] = {
            "label": label,
            "company_id": None if anonymise else cid,
            "status": seat.get("status"),
        }
        try:
            if cid and company_dir(cid).is_dir():
                st = status.collect_status(cid)
                row["score"] = st.get("score")
                row["band"] = st.get("band")
                row["pipeline_active"] = st.get("snapshot", {}).get("pipeline_active")
                row["weekly_reports"] = st.get("snapshot", {}).get("weekly_reports")
                row["gaps"] = [g.get("area") for g in (st.get("gaps") or [])[:5]]
                if isinstance(st.get("score"), int):
                    scores.append(int(st["score"]))
            else:
                row["score"] = None
                row["band"] = "missing_memory"
                row["gaps"] = ["company_memory"]
        except Exception as e:  # noqa: BLE001
            row["score"] = None
            row["band"] = "error"
            row["error"] = str(e)
        seat_rows.append(row)

    avg = round(sum(scores) / len(scores), 1) if scores else None
    report = {
        "cohort_id": cfg.get("cohort_id"),
        "partner_name": cfg.get("partner_name"),
        "programme": cfg.get("programme"),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": date.today().isoformat(),
        "anonymised": anonymise,
        "seat_quota": cfg.get("seat_quota"),
        "seats_active": len(seats),
        "avg_score": avg,
        "seats": seat_rows,
        "hitl": "Partner report is informational. Deliver manually — agent does not email.",
        "recommendations": _recommendations(seat_rows, avg),
    }
    return report


def _recommendations(rows: list[dict[str, Any]], avg: float | None) -> list[str]:
    recs = []
    missing = sum(1 for r in rows if r.get("band") in {"missing_memory", "error", None})
    early = sum(1 for r in rows if r.get("band") == "early")
    if missing:
        recs.append(f"{missing} seat(s) missing company memory — re-run onboard or add-seat")
    if early:
        recs.append(f"{early} seat(s) early — push weekly board + pipeline discipline")
    if avg is not None and avg < 50:
        recs.append("Cohort average under 50 — run group workshop on weekly board + paid pilots")
    if not recs:
        recs.append("Cohort healthy enough for mentor board-pack reviews this week")
    return recs


def write_partner_report(
    cohort_id: str,
    *,
    anonymise: bool = False,
) -> tuple[dict[str, Any], Path]:
    report = build_partner_report(cohort_id, anonymise=anonymise)
    cdir = cohorts_root() / cohort_id / "reports"
    cdir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    suffix = "anon" if anonymise else "named"
    md_path = cdir / f"partner-report-{suffix}-{stamp}.md"
    json_path = cdir / f"partner-report-{suffix}-{stamp}.json"
    latest = cdir / f"partner-report-{suffix}-latest.md"
    md = format_partner_report_markdown(report)
    md_path.write_text(md, encoding="utf-8", newline="\n")
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    latest.write_text(md, encoding="utf-8", newline="\n")
    return report, latest


def format_partner_report_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Partner report — {report.get('partner_name')}",
        "",
        f"- Cohort: `{report.get('cohort_id')}`",
        f"- Programme: {report.get('programme')}",
        f"- Seats: {report.get('seats_active')} / {report.get('seat_quota')}",
        f"- Average score: {report.get('avg_score')}",
        f"- Anonymised: {report.get('anonymised')}",
        f"- Generated: {report.get('generated_at')}",
        "",
        report.get("hitl", ""),
        "",
        "## Seats",
        "",
        "| Label | Score | Band | Pipeline active | Weekly | Top gaps |",
        "|-------|-------|------|-----------------|--------|----------|",
    ]
    for s in report.get("seats") or []:
        gaps = ", ".join(s.get("gaps") or []) or "—"
        lines.append(
            f"| {s.get('label')} | {s.get('score')} | {s.get('band')} | "
            f"{s.get('pipeline_active')} | {s.get('weekly_reports')} | {gaps} |"
        )
    lines.extend(["", "## Recommendations", ""])
    for r in report.get("recommendations") or []:
        lines.append(f"- {r}")
    lines.append("")
    return "\n".join(lines)
