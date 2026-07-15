"""G7 — Long-horizon task state per company."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

STATUSES = ("todo", "in_progress", "blocked", "done", "cancelled")


def tasks_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "tasks.jsonl"


def append_task(
    company_id: str,
    *,
    title: str,
    owner: str = "Founder",
    skill: str = "board-chief-of-staff",
    status: str = "todo",
    next_step: str = "",
    due: str = "",
    notes: str = "",
) -> dict[str, Any]:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    if not title.strip():
        raise ValueError("title required")
    path = tasks_path(company_id)
    task_id = f"T{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    row = {
        "id": task_id,
        "title": title.strip(),
        "owner": owner,
        "skill": skill,
        "status": status,
        "next_step": next_step,
        "due": due or "",
        "notes": notes,
        "updated": date.today().isoformat(),
        "created": date.today().isoformat(),
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    _sync_md(company_id)
    append_audit(
        ensure_exists(company_id),
        actor=f"agent:{skill}",
        skill=skill,
        action="task_append",
        summary=f"{task_id} {title[:80]}",
        artefact_ref="tasks.jsonl",
        model_tier="light",
        tokens_in=0,
        tokens_out=0,
        outcome="ok",
    )
    return row


def list_tasks(company_id: str, *, status: str | None = None) -> list[dict[str, Any]]:
    path = tasks_path(company_id)
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    # last write wins per id
    by_id: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            tid = row.get("id") or ""
            if tid:
                by_id[tid] = row
    rows = list(by_id.values())
    if status:
        rows = [r for r in rows if r.get("status") == status]
    rows.sort(key=lambda r: (r.get("status") != "in_progress", r.get("due") or "9999", r.get("id") or ""))
    return rows


def update_task(
    company_id: str,
    task_id: str,
    *,
    status: str | None = None,
    next_step: str | None = None,
    notes: str | None = None,
    owner: str | None = None,
) -> dict[str, Any]:
    existing = {t["id"]: t for t in list_tasks(company_id)}
    if task_id not in existing:
        raise FileNotFoundError(f"Unknown task {task_id}")
    row = dict(existing[task_id])
    if status is not None:
        if status not in STATUSES:
            raise ValueError(f"status must be one of {STATUSES}")
        row["status"] = status
    if next_step is not None:
        row["next_step"] = next_step
    if notes is not None:
        row["notes"] = notes
    if owner is not None:
        row["owner"] = owner
    row["updated"] = date.today().isoformat()
    path = tasks_path(company_id)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    _sync_md(company_id)
    append_audit(
        ensure_exists(company_id),
        actor="agent:board-chief-of-staff",
        skill="board-chief-of-staff",
        action="task_update",
        summary=f"{task_id} → {row.get('status')}",
        artefact_ref="tasks.jsonl",
        model_tier="light",
        outcome="ok",
    )
    return row


def _sync_md(company_id: str) -> None:
    rows = list_tasks(company_id)
    lines = [
        "# Tasks (long-horizon)",
        "",
        "Board skill reads this first. Specialists append/update. Single-writer rule applies.",
        "",
        "| ID | Status | Owner | Skill | Title | Next step | Due |",
        "|----|--------|-------|-------|-------|-----------|-----|",
    ]
    for r in rows:
        if r.get("status") == "done":
            continue
        lines.append(
            f"| {r.get('id')} | {r.get('status')} | {r.get('owner')} | {r.get('skill')} | "
            f"{r.get('title')} | {r.get('next_step')} | {r.get('due')} |"
        )
    lines.append("")
    (ensure_exists(company_id) / "tasks.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
