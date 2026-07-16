# Audit Log Schema

JSONL recommended path: `memory/companies/<id>/audit.jsonl`

```json
{
 "ts": "2026-07-15T12:00:00Z",
 "actor": "agent:grants-rdti-clerk",
 "skill": "grants-rdti-clerk",
 "action": "draft_rdti_log_entry",
 "tier": "platinum",
 "hitl_required": false,
 "hitl_status": "n/a",
 "artefact_ref": "memory/companies/demo/rdti-log.csv#row-12",
 "summary": "Drafted RDTI row from commit abc123",
 "risk_level": "low",
 "outcome": "ok",
 "model": "grok-4.5",
 "model_tier": "light",
 "tokens_in": 1200,
 "tokens_out": 400,
 "duration_ms": 850,
 "est_cost_nzd": 0.0032
}
```

## Required fields

| Field | Type | Notes |
|-------|------|-------|
| ts | ISO-8601 | UTC |
| actor | string | `agent:<skill>` or `human:<id>` |
| skill | string | skill name |
| action | string | verb_snake |
| hitl_required | bool | |
| hitl_status | enum | n/a \| pending \| approved \| rejected |
| summary | string | one line, no secrets |

## Telemetry fields (G8 - optional but preferred)

| Field | Type | Notes |
|-------|------|-------|
| outcome | string | ok \| error \| blocked |
| model | string | provider model id if known |
| model_tier | enum | light \| standard \| frontier |
| tokens_in / tokens_out | int | when metered |
| duration_ms | int | wall time |
| est_cost_nzd | float | heuristic NZD (board pack fleet-cost line) |

## Actions that must log

- Any draft of legal, finance, grant, or outreach artefacts 
- Any memory write of material decisions 
- Any HITL request or resolution 
- Any export of company memory 
