"""Weekly operating review generator."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from nz_startup import calendar_ops, grants, pipeline
from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists, read_file
from nz_startup.paths import templates_dir


def generate_weekly_review(company_id: str, review_date: str | None = None) -> Path:
    company = ensure_exists(company_id)
    d = review_date or date.today().isoformat()
    template_path = templates_dir() / "weekly-operating-review.md"
    if template_path.is_file():
        body = template_path.read_text(encoding="utf-8").replace("{{date}}", d)
    else:
        body = f"# Weekly Operating Review — {d}\n\n"

    # Structured board slices (v0.3)
    try:
        pipe_md = pipeline.format_summary_markdown(company_id)
    except Exception as e:  # noqa: BLE001 — board still ships if slice fails
        pipe_md = f"_Pipeline unavailable: {e}_"
    try:
        cal_md = calendar_ops.format_reminders_markdown(company_id, within_days=14)
    except Exception as e:  # noqa: BLE001
        cal_md = f"_Calendar unavailable: {e}_"
    try:
        grants_md = grants.format_board_slice(company_id)
    except Exception as e:  # noqa: BLE001
        grants_md = f"_Grants unavailable: {e}_"

    # Inject lightweight memory snapshots (truncated)
    snippets = []
    for rel, label in (
        ("pipeline.md", "Pipeline file"),
        ("runway.md", "Runway"),
        ("calendar.md", "Calendar file"),
        ("grants-tracker.md", "Grants tracker file"),
    ):
        try:
            text = read_file(company_id, rel)
            snippets.append(f"### {label} (snapshot)\n\n```markdown\n{text[:1200]}\n```\n")
        except FileNotFoundError:
            snippets.append(f"### {label}\n\n_Missing {rel}_\n")

    out = (
        body.rstrip()
        + "\n\n---\n\n## Live fleet board (auto)\n\n"
        + pipe_md
        + "\n\n"
        + cal_md
        + "\n\n"
        + grants_md
        + "\n\n---\n\n## Memory snapshots\n\n"
        + "\n".join(snippets)
        + "\n\n## HITL reminder\n\n"
        + "Agents escalate; founders decide, file, send, and pay.\n"
    )
    dest = company / "weekly" / f"{d}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8", newline="\n")
    append_audit(
        company,
        actor="agent:board-chief-of-staff",
        skill="board-chief-of-staff",
        action="generate_weekly_review",
        summary=f"Weekly review {d}",
        artefact_ref=f"weekly/{d}.md",
        tier="platinum",
        hitl_required=True,
        hitl_status="pending",
        risk_level="medium",
    )
    return dest
