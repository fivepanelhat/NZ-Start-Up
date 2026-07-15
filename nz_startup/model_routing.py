"""G9/T6 — Model tier routing + per-company monthly token budget with hard caps."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup.memory import ensure_exists
from nz_startup.paths import repo_root

TIERS = ("light", "standard", "frontier")

DEFAULT_SKILL_TIERS: dict[str, str] = {
    "finance-clerk": "light",
    "grants-rdti-clerk": "light",
    "gtm-pipeline-rep": "standard",
    "content-comms-officer": "standard",
    "board-chief-of-staff": "standard",
    "market-validator": "standard",
    "formation-officer": "standard",
    "funding-analyst": "frontier",
    "legal-document-assistant": "frontier",
    "compliance-registrar": "standard",
    "agent-hardening": "light",
    "nz-startup-fleet": "standard",
    "cat-architectural-standards": "light",
}

DEFAULT_MONTHLY_TOKEN_BUDGET = 2_000_000
DEFAULT_WARN_FRACTION = 0.8


class BudgetExceededError(PermissionError):
    """Hard cap enforced — human must raise budget."""


def resolve_tier(skill: str = "", explicit: str = "") -> str:
    if explicit and explicit in TIERS:
        return explicit
    key = (skill or "").strip().lower()
    return DEFAULT_SKILL_TIERS.get(key, "standard")


def budget_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "budget.json"


def load_budget(company_id: str) -> dict[str, Any]:
    path = budget_path(company_id)
    if not path.is_file():
        return {
            "monthly_token_budget": DEFAULT_MONTHLY_TOKEN_BUDGET,
            "warn_fraction": DEFAULT_WARN_FRACTION,
            "enforce": False,
            "month": date.today().strftime("%Y-%m"),
            "tokens_used": 0,
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {}
    month = date.today().strftime("%Y-%m")
    if data.get("month") != month:
        data["month"] = month
        data["tokens_used"] = 0
    data.setdefault("monthly_token_budget", DEFAULT_MONTHLY_TOKEN_BUDGET)
    data.setdefault("warn_fraction", DEFAULT_WARN_FRACTION)
    data.setdefault("enforce", False)
    data.setdefault("tokens_used", 0)
    return data


def save_budget(company_id: str, data: dict[str, Any]) -> Path:
    path = budget_path(company_id)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def check_allowed(
    company_id: str,
    *,
    model_tier: str = "standard",
    skill: str = "",
) -> dict[str, Any]:
    """
    T6 — if enforce=true and budget exhausted, refuse frontier (and optionally all) work.
    """
    data = load_budget(company_id)
    tier = resolve_tier(skill, model_tier)
    used = int(data.get("tokens_used") or 0)
    budget = int(data.get("monthly_token_budget") or DEFAULT_MONTHLY_TOKEN_BUDGET)
    warn_at = int(budget * float(data.get("warn_fraction") or DEFAULT_WARN_FRACTION))
    enforce = bool(data.get("enforce"))
    exhausted = used >= budget
    warning = used >= warn_at
    allowed = True
    reason = "ok"
    if enforce and exhausted and tier == "frontier":
        allowed = False
        reason = (
            "Hard token budget exhausted — frontier-tier work blocked until a human "
            "raises the monthly cap (nz-startup budget set --tokens N)."
        )
    elif enforce and exhausted:
        # soft block only frontier by default; light/standard may continue with warning
        reason = "budget exhausted (enforce=true) — frontier blocked; light/standard allowed with warning"
    return {
        "allowed": allowed,
        "reason": reason,
        "model_tier": tier,
        "warning": warning,
        "exhausted": exhausted,
        "enforce": enforce,
        "tokens_used": used,
        "monthly_token_budget": budget,
    }


def record_usage(
    company_id: str,
    tokens_in: int = 0,
    tokens_out: int = 0,
    *,
    skill: str = "",
    model_tier: str = "",
    enforce_check: bool = True,
) -> dict[str, Any]:
    tier = resolve_tier(skill, model_tier)
    if enforce_check:
        gate = check_allowed(company_id, model_tier=tier, skill=skill)
        if not gate["allowed"]:
            raise BudgetExceededError(gate["reason"])
    data = load_budget(company_id)
    used = int(data.get("tokens_used") or 0) + int(tokens_in or 0) + int(tokens_out or 0)
    data["tokens_used"] = used
    budget = int(data.get("monthly_token_budget") or DEFAULT_MONTHLY_TOKEN_BUDGET)
    warn_at = int(budget * float(data.get("warn_fraction") or DEFAULT_WARN_FRACTION))
    data["warning"] = used >= warn_at
    data["exhausted"] = used >= budget
    data["last_skill"] = skill
    data["last_tier"] = tier
    save_budget(company_id, data)
    return data


def skill_frontmatter_tiers() -> dict[str, str]:
    root = repo_root() / "skills"
    out: dict[str, str] = {}
    if not root.is_dir():
        return out
    for skill_dir in root.iterdir():
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        fm = text[3:end]
        for line in fm.splitlines():
            if line.strip().startswith("model_tier:"):
                val = line.split(":", 1)[1].strip().strip("\"'")
                if val in TIERS:
                    out[skill_dir.name] = val
    return out


def routing_status(company_id: str | None = None) -> dict[str, Any]:
    tiers = {**DEFAULT_SKILL_TIERS, **skill_frontmatter_tiers()}
    result: dict[str, Any] = {
        "tiers": list(TIERS),
        "skill_tiers": tiers,
        "default_monthly_token_budget": DEFAULT_MONTHLY_TOKEN_BUDGET,
        "hard_cap_supported": True,
    }
    if company_id:
        result["budget"] = load_budget(company_id)
        result["gate"] = check_allowed(company_id)
    return result
