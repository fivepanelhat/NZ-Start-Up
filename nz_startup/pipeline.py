"""CRM-lite pipeline — drafts and stage tracking only (never sends)."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

STAGES = (
    "lead",
    "discovery",
    "qualified",
    "proposal",
    "pilot",
    "negotiation",
    "won",
    "lost",
    "nurture",
)

FIELDS = [
    "id",
    "account",
    "stage",
    "next_step",
    "owner",
    "value_nzd",
    "source",
    "last_touch",
    "notes",
]


def csv_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "pipeline.csv"


def md_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "pipeline.md"


def ensure_csv(company_id: str) -> Path:
    path = csv_path(company_id)
    if not path.exists() or path.stat().st_size == 0:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()
    return path


def _read_rows(company_id: str) -> list[dict[str, str]]:
    path = ensure_csv(company_id)
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_rows(company_id: str, rows: list[dict[str, str]]) -> None:
    path = ensure_csv(company_id)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    _sync_markdown(company_id, rows)


def _sync_markdown(company_id: str, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Pipeline",
        "",
        "| ID | Account | Stage | Next step | Owner | Value NZD | Last touch |",
        "|----|---------|-------|-----------|-------|-----------|------------|",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('id','')} | {r.get('account','')} | {r.get('stage','')} | "
            f"{r.get('next_step','')} | {r.get('owner','')} | {r.get('value_nzd','')} | "
            f"{r.get('last_touch','')} |"
        )
    lines.append("")
    lines.append(
        "_CRM is local and drafts-only. Outreach sends require human action (UEM Act)._"
    )
    md_path(company_id).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _next_id(rows: list[dict[str, str]]) -> str:
    nums = []
    for r in rows:
        rid = (r.get("id") or "").strip()
        if rid.startswith("P") and rid[1:].isdigit():
            nums.append(int(rid[1:]))
    n = max(nums) + 1 if nums else 1
    return f"P{n:03d}"


def list_deals(
    company_id: str,
    *,
    stage: str | None = None,
) -> list[dict[str, str]]:
    rows = _read_rows(company_id)
    if stage:
        s = stage.lower().strip()
        rows = [r for r in rows if (r.get("stage") or "").lower() == s]
    return rows


def add_deal(
    company_id: str,
    *,
    account: str,
    stage: str = "lead",
    next_step: str = "",
    owner: str = "Founder",
    value_nzd: str = "",
    source: str = "",
    notes: str = "",
) -> dict[str, str]:
    stage_l = stage.lower().strip()
    if stage_l not in STAGES:
        raise ValueError(f"Invalid stage '{stage}'. Allowed: {', '.join(STAGES)}")
    if not account.strip():
        raise ValueError("account is required")
    rows = _read_rows(company_id)
    row = {
        "id": _next_id(rows),
        "account": account.strip(),
        "stage": stage_l,
        "next_step": next_step.strip(),
        "owner": owner.strip() or "Founder",
        "value_nzd": value_nzd.strip(),
        "source": source.strip(),
        "last_touch": date.today().isoformat(),
        "notes": notes.strip(),
    }
    rows.append(row)
    _write_rows(company_id, rows)
    append_audit(
        ensure_exists(company_id),
        actor="agent:gtm-pipeline-rep",
        skill="gtm-pipeline-rep",
        action="pipeline_add_deal",
        summary=f"{row['id']} {row['account']} → {row['stage']}",
        artefact_ref="pipeline.csv",
        tier="gold",
    )
    return row


def update_deal(
    company_id: str,
    deal_id: str,
    *,
    stage: str | None = None,
    next_step: str | None = None,
    owner: str | None = None,
    value_nzd: str | None = None,
    notes: str | None = None,
    touch: bool = True,
) -> dict[str, str]:
    rows = _read_rows(company_id)
    found = None
    for r in rows:
        if r.get("id") == deal_id:
            found = r
            break
    if not found:
        raise FileNotFoundError(f"Unknown deal id: {deal_id}")
    if stage is not None:
        stage_l = stage.lower().strip()
        if stage_l not in STAGES:
            raise ValueError(f"Invalid stage '{stage}'. Allowed: {', '.join(STAGES)}")
        found["stage"] = stage_l
    if next_step is not None:
        found["next_step"] = next_step
    if owner is not None:
        found["owner"] = owner
    if value_nzd is not None:
        found["value_nzd"] = value_nzd
    if notes is not None:
        found["notes"] = notes
    if touch:
        found["last_touch"] = date.today().isoformat()
    _write_rows(company_id, rows)
    append_audit(
        ensure_exists(company_id),
        actor="agent:gtm-pipeline-rep",
        skill="gtm-pipeline-rep",
        action="pipeline_update_deal",
        summary=f"{deal_id} stage={found.get('stage')} next={found.get('next_step','')[:60]}",
        artefact_ref="pipeline.csv",
        tier="gold",
    )
    return found


def summary(company_id: str) -> dict[str, Any]:
    rows = _read_rows(company_id)
    by_stage: dict[str, int] = {s: 0 for s in STAGES}
    for r in rows:
        s = (r.get("stage") or "lead").lower()
        by_stage[s] = by_stage.get(s, 0) + 1
    active = [r for r in rows if r.get("stage") not in ("won", "lost")]
    return {
        "total": len(rows),
        "active": len(active),
        "by_stage": by_stage,
        "deals": rows,
    }


def format_summary_markdown(company_id: str) -> str:
    s = summary(company_id)
    lines = [
        "# Pipeline summary",
        "",
        f"- Total deals: {s['total']}",
        f"- Active (not won/lost): {s['active']}",
        "",
        "## By stage",
        "",
    ]
    for stage, n in s["by_stage"].items():
        if n:
            lines.append(f"- **{stage}**: {n}")
    lines.append("")
    lines.append("## Active next steps")
    lines.append("")
    for r in s["deals"]:
        if r.get("stage") in ("won", "lost"):
            continue
        lines.append(
            f"- `{r.get('id')}` **{r.get('account')}** [{r.get('stage')}] — "
            f"{r.get('next_step') or '_no next step_'}"
        )
    lines.append("")
    lines.append("DRAFT — human owns all outbound contact.")
    return "\n".join(lines)
