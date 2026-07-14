"""Append-only JSONL audit log."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def append_audit(
    company_path: Path,
    *,
    actor: str,
    skill: str,
    action: str,
    summary: str,
    hitl_required: bool = False,
    hitl_status: str = "n/a",
    tier: str = "gold",
    risk_level: str = "low",
    artefact_ref: str = "",
    extra: dict[str, Any] | None = None,
) -> Path:
    path = company_path / "audit.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "actor": actor,
        "skill": skill,
        "action": action,
        "tier": tier,
        "hitl_required": hitl_required,
        "hitl_status": hitl_status,
        "artefact_ref": artefact_ref,
        "summary": summary[:500],
        "risk_level": risk_level,
    }
    if extra:
        event["extra"] = extra
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return path
