"""
Mentor / board pack — zip for EDA mentors and advisors (not full accountant dump).

Emphasises weekly board, pipeline, grants, status, demo report.
Does not email.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from nz_startup import status as status_mod
from nz_startup import weekly
from nz_startup.audit import append_audit, sum_costs
from nz_startup.memory import ensure_exists
from nz_startup.memory_index import write_index

BOARD_GLOBS = [
    "INDEX.md",
    "profile.md",
    "tasks.md",
    "pipeline.md",
    "pipeline.csv",
    "calendar.md",
    "calendar.csv",
    "grants-tracker.md",
    "grants-tracker.csv",
    "runway.md",
    "rdti-log.csv",
    "weekly/*",
    "status/status-latest.md",
    "status/status-latest.json",
    "demo/demo-report-latest.md",
    "exports/deadline-digest-latest.md",
    "exports/deadlines-latest.ics",
    "decisions.md",
]


def _iter_files(company: Path) -> list[Path]:
    found: set[Path] = set()
    for pattern in BOARD_GLOBS:
        for p in company.glob(pattern):
            if p.is_file():
                name = p.name.lower()
                if any(x in name for x in ("password", "secret", "token", ".env")):
                    continue
                found.add(p)
    return sorted(found, key=lambda x: str(x))


def create_board_pack(
    company_id: str,
    *,
    label: str = "mentor",
    refresh_weekly: bool = True,
    refresh_status: bool = True,
) -> dict[str, Path | int | str]:
    company = ensure_exists(company_id)

    if refresh_status:
        status_mod.write_status(company_id)
    if refresh_weekly:
        weekly.generate_weekly_review(company_id)
    write_index(company_id)
    fleet_cost = sum_costs(company)

    files = _iter_files(company)
    out_dir = company / "board-packs"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    zip_path = out_dir / f"board-pack-{label}-{stamp}.zip"
    latest = out_dir / "board-pack-latest.zip"

    manifest = {
        "purpose": "Mentor / board / EDA pack — operating review artefacts",
        "company_id": company_id,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "not_legal_or_financial_advice": True,
        "hitl": "For human discussion only. Agent does not email this pack.",
        "file_count": len(files),
        "files": [str(p.relative_to(company)).replace("\\", "/") for p in files],
        "fleet_cost": fleet_cost,
        "suggested_agenda": [
            "Pipeline vs plan (pipeline.md / status)",
            "Cash / runway narrative (runway.md — figures human-owned)",
            "Compliance deadlines (calendar / digest)",
            "RDTI log hygiene",
            f"Fleet cost (heuristic NZD): ${fleet_cost.get('est_cost_nzd')} across {fleet_cost.get('entries')} metered events",
            "Top 3 founder decisions this week",
        ],
    }
    readme = _readme(manifest)

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("BOARD_README.md", readme)
        zf.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
        for p in files:
            zf.write(p, arcname=str(p.relative_to(company)).replace("\\", "/"))

    latest.write_bytes(zip_path.read_bytes())
    (out_dir / "BOARD_README.md").write_text(readme, encoding="utf-8", newline="\n")

    append_audit(
        company,
        actor="agent:board-chief-of-staff",
        skill="board-chief-of-staff",
        action="board_pack_create",
        summary=f"Board/mentor pack {zip_path.name} ({len(files)} files)",
        artefact_ref=str(zip_path.relative_to(company)).replace("\\", "/"),
        tier="platinum",
        hitl_required=True,
        hitl_status="pending",
    )
    return {
        "zip": zip_path,
        "latest": latest,
        "file_count": len(files),
        "readme": out_dir / "BOARD_README.md",
    }


def _readme(manifest: dict) -> str:
    lines = [
        "# Board / mentor pack",
        "",
        f"- Company: `{manifest['company_id']}`",
        f"- Generated: {manifest['generated_at']}",
        f"- Files: {manifest['file_count']}",
        f"- Est. fleet cost (NZD heuristic): **${(manifest.get('fleet_cost') or {}).get('est_cost_nzd', 0)}**",
        "",
        "## Purpose",
        "",
        "Operating review pack for mentors, EDAs, and boards.",
        "Not a tax handoff (use `nz-startup handoff pack` for accountants).",
        "",
        "## Suggested agenda",
        "",
    ]
    for a in manifest.get("suggested_agenda") or []:
        lines.append(f"- {a}")
    lines.extend(
        [
            "",
            "## HITL",
            "",
            manifest.get("hitl", ""),
            "",
            "**Not legal or financial advice.**",
            "",
            "## Files",
            "",
        ]
    )
    for f in manifest.get("files") or []:
        lines.append(f"- `{f}`")
    lines.append("")
    return "\n".join(lines)
