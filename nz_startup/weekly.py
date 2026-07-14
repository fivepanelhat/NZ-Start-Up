"""Weekly operating review generator."""
from __future__ import annotations

from datetime import date
from pathlib import Path

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

    # Inject lightweight memory snapshots (truncated)
    snippets = []
    for rel, label in (
        ("pipeline.md", "Pipeline"),
        ("runway.md", "Runway"),
        ("calendar.md", "Calendar"),
    ):
        try:
            text = read_file(company_id, rel)
            snippets.append(f"### {label} (snapshot)\n\n```markdown\n{text[:1500]}\n```\n")
        except FileNotFoundError:
            snippets.append(f"### {label}\n\n_Missing {rel}_\n")

    out = (
        body.rstrip()
        + "\n\n---\n\n## Memory snapshots (auto)\n\n"
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
