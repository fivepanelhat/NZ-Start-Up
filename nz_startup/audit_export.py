"""T8 — Export audit.jsonl as OTel-GenAI-shaped JSON (no OTel dependency)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup.memory import ensure_exists


def _to_otlp_span(event: dict[str, Any], company_id: str) -> dict[str, Any]:
    """Map one audit row to a simplified GenAI-ish span object."""
    ts = event.get("ts") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    attrs = {
        "gen_ai.system": "nz-startup-in-a-box",
        "gen_ai.request.model": event.get("model") or "",
        "gen_ai.request.model_tier": event.get("model_tier") or "",
        "gen_ai.usage.input_tokens": event.get("tokens_in"),
        "gen_ai.usage.output_tokens": event.get("tokens_out"),
        "gen_ai.operation.name": event.get("action") or "unknown",
        "nz.startup.skill": event.get("skill") or "",
        "nz.startup.actor": event.get("actor") or "",
        "nz.startup.company_id": company_id,
        "nz.startup.hitl_required": event.get("hitl_required"),
        "nz.startup.hitl_status": event.get("hitl_status"),
        "nz.startup.risk_level": event.get("risk_level"),
        "nz.startup.outcome": event.get("outcome"),
        "nz.startup.est_cost_nzd": event.get("est_cost_nzd"),
        "nz.startup.artefact_ref": event.get("artefact_ref") or "",
        "nz.startup.summary": (event.get("summary") or "")[:500],
    }
    # drop nulls
    attrs = {k: v for k, v in attrs.items() if v is not None and v != ""}
    return {
        "name": f"nz.startup.{event.get('action') or 'event'}",
        "startTimeUnixNano": None,  # wall clock only in attributes
        "endTimeUnixNano": None,
        "attributes": attrs,
        "ts": ts,
        "duration_ms": event.get("duration_ms"),
        "status": {
            "code": "OK" if (event.get("outcome") or "ok") == "ok" else "ERROR",
            "message": event.get("summary") or "",
        },
    }


def export_audit(
    company_id: str,
    *,
    format: str = "otel-json",  # otel-json | jsonl | otlp-file
    out_path: Path | None = None,
    limit: int = 0,
) -> dict[str, Any]:
    company = ensure_exists(company_id)
    src = company / "audit.jsonl"
    events: list[dict[str, Any]] = []
    if src.is_file():
        with src.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    if limit > 0:
        events = events[-limit:]

    if format == "jsonl":
        payload_lines = [json.dumps(e, ensure_ascii=False) for e in events]
        text = "\n".join(payload_lines) + ("\n" if payload_lines else "")
        payload: Any = None
    else:
        spans = [_to_otlp_span(e, company_id) for e in events]
        payload = {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": {
                            "service.name": "nz-startup-in-a-box",
                            "service.version": __import__("nz_startup").__version__,
                            "nz.startup.company_id": company_id,
                        }
                    },
                    "scopeSpans": [
                        {
                            "scope": {"name": "nz.startup.audit", "version": "1.6.0"},
                            "spans": spans,
                        }
                    ],
                }
            ],
            "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "entry_count": len(spans),
            "format": "otel-genai-shaped-json-v1",
            "note": "Not a live OTLP push — convertible shape for partner observability stacks.",
        }
        text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    out_dir = company / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    if out_path is None:
        suffix = "jsonl" if format == "jsonl" else "otel.json"
        out_path = out_dir / f"audit-export-{suffix if format == 'jsonl' else 'otel.json'}"
        if format != "jsonl":
            out_path = out_dir / "audit-export-otel.json"
        else:
            out_path = out_dir / "audit-export.jsonl"
    out_path = Path(out_path)
    out_path.write_text(text, encoding="utf-8")
    latest = out_dir / ("audit-export-latest.jsonl" if format == "jsonl" else "audit-export-otel-latest.json")
    latest.write_text(text, encoding="utf-8")
    return {
        "company_id": company_id,
        "format": format,
        "entries": len(events),
        "path": str(out_path),
        "latest": str(latest),
    }
