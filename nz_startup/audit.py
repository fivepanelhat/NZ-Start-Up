"""Append-only JSONL audit log with optional telemetry (G8/T6).

NZD/token rates carry verified dates so freshness CI can catch stale economics.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Rough NZD/token heuristic for board pack cost lines (not a billing system)
# T6 - verified: date for freshness of economics
COST_RATES_META = {
 "verified": "2026-07-15",
 "currency": "NZD",
 "unit": "per_1k_tokens",
 "note": "Heuristic only - re-verify before board packs quote costs to partners.",
}
_DEFAULT_NZD_PER_1K_TOKENS = {
 "light": 0.002,
 "standard": 0.02,
 "frontier": 0.12,
}


def cost_rates() -> dict[str, Any]:
 return {
 **COST_RATES_META,
 "rates": dict(_DEFAULT_NZD_PER_1K_TOKENS),
 }


def estimate_cost_nzd(
 tokens_in: int = 0,
 tokens_out: int = 0,
 model_tier: str = "standard",
) -> float:
 rate = _DEFAULT_NZD_PER_1K_TOKENS.get(model_tier, _DEFAULT_NZD_PER_1K_TOKENS["standard"])
 return round(((tokens_in + tokens_out) / 1000.0) * rate, 4)


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
 # G8 telemetry
 model: str = "",
 model_tier: str = "",
 tokens_in: int | None = None,
 tokens_out: int | None = None,
 duration_ms: int | None = None,
 est_cost_nzd: float | None = None,
 outcome: str = "ok",
) -> Path:
 path = company_path / "audit.jsonl"
 path.parent.mkdir(parents=True, exist_ok=True)
 tin = int(tokens_in or 0)
 tout = int(tokens_out or 0)
 mtier = model_tier or "standard"
 cost = est_cost_nzd
 if cost is None and (tin or tout):
 cost = estimate_cost_nzd(tin, tout, mtier)
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
 "outcome": outcome,
 "model": model,
 "model_tier": mtier if model or model_tier else "",
 "tokens_in": tin if tokens_in is not None else None,
 "tokens_out": tout if tokens_out is not None else None,
 "duration_ms": duration_ms,
 "est_cost_nzd": cost,
 "cost_rates_verified": COST_RATES_META["verified"] if cost is not None else None,
 }
 if extra:
 event["extra"] = extra
 with path.open("a", encoding="utf-8") as f:
 f.write(json.dumps(event, ensure_ascii=False) + "\n")
 return path


def sum_costs(company_path: Path, *, since_prefix: str = "") -> dict[str, Any]:
 """Sum est_cost_nzd from audit.jsonl for board pack fleet-cost line."""
 path = company_path / "audit.jsonl"
 total = 0.0
 n = 0
 if not path.is_file():
 return {
 "entries": 0,
 "est_cost_nzd": 0.0,
 "cost_rates_verified": COST_RATES_META["verified"],
 }
 with path.open(encoding="utf-8") as f:
 for line in f:
 line = line.strip()
 if not line:
 continue
 try:
 ev = json.loads(line)
 except json.JSONDecodeError:
 continue
 if since_prefix and not str(ev.get("ts", "")).startswith(since_prefix):
 continue
 c = ev.get("est_cost_nzd")
 if c is not None:
 try:
 total += float(c)
 n += 1
 except (TypeError, ValueError):
 pass
 return {
 "entries": n,
 "est_cost_nzd": round(total, 4),
 "cost_rates_verified": COST_RATES_META["verified"],
 }
