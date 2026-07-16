# Agent Hardening Guide

**Version:** 1.3 | Coastal Alpine Tech | NZ Start-Up in a Box | Portfolio pack aligned

## Autonomy ceiling

| Agents may | Humans must |
|------------|-------------|
| Inform | Advise |
| Draft | Sign |
| Prepare | File |
| Monitor | Send |
| Remind | Pay |

## Anti-hallucination (portfolio standard)

| Mechanism | Where |
|-----------|--------|
| Prefer tools/files over model memory | `AGENTS.md`, `.github/agent-fleet/anti-hallucination.md` |
| FACT / INFERENCE / UNKNOWN labels | anti-hallucination policy |
| Refusal when evidence missing | agent-hardening v1.1 + HITL default-deny |
| Extended thinking before high-stakes answers | list unknowns & failure modes first |
| Knowledge freshness 90-day gate | `knowledge/*` `verified:` + CI |
| Untrusted inbound quarantine | `nz_startup/untrusted.py` (nonce fences) |
| No invented MCP tools | MCP surface never exposes send/file/pay |

**Investor/reviewer signal:** we would rather refuse or mark `NEEDS_EVIDENCE` than invent NZBN, LOIs, stats, or partnerships.

## Enforcement layers

```text
User / Aether / Claude / Grok
 |
 
-------------------
| agent-hardening | policy skill + anti-hallucination
| anti-hallucination.md
`------------------
 
-------------------
| hitl.py | default-deny allow-list + fragments
| agent_guardrails | risk tier, secrets, sandbox, watermarks
| untrusted.py | inbound data quarantine
`------------------
 
-------------------
| MCP / CLI runtime | no send/file/pay tools exist
`------------------
 
-------------------
| Company memory | path sandbox + audit.jsonl + INDEX
`-------------------
```

## Specialist risk map

| Skill | Default risk | HITL |
|-------|--------------|------|
| market-validator | low-medium | sources required |
| content-comms-officer | medium | publish pre-approved only |
| formation-officer | high | founder files RealMe |
| compliance-registrar | high | never self-certify |
| grants-rdti-clerk | high | human submits |
| gtm-pipeline-rep | high | DRAFT_NOT_SENT |
| finance-clerk | high | no money movement |
| funding-analyst | high | FMCA boundary |
| legal-document-assistant | critical | not legal advice |
| board-chief-of-staff | medium | escalates, never decides |

## Secret refusal

Runtime refuses writes containing:

- PEM / private keys 
- AWS-style access keys 
- API key / secret assignments 
- JWT bearer tokens 
- DB URLs with embedded passwords 

## Path sandbox

All company file IO must resolve under `memory/companies/<id>/` with no `..` segments.

## CLI

```bash
nz-startup harden status
nz-startup harden check --action "send outreach email"
nz-startup harden check --action "draft weekly board" --skill board-chief-of-staff
```

## MCP

- `harden_status` - policy snapshot 
- `harden_check` - classify an action 

## Related

- `compliance/hitl-matrix.md` 
- `COMPLIANCE.md` 
- Aether `guardrails.py` / `COMPLIANCE.md` 
