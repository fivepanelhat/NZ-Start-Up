# Agent Hardening Guide

**Version:** 1.2 · Coastal Alpine Tech · NZ Start-Up in a Box

## Autonomy ceiling

| Agents may | Humans must |
|------------|-------------|
| Inform | Advise |
| Draft | Sign |
| Prepare | File |
| Monitor | Send |
| Remind | Pay |

## Enforcement layers

```text
User / Aether / Claude
        │
        ▼
┌───────────────────┐
│ agent-hardening   │  policy skill (always load first with CAT standards)
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ hitl.py           │  forbidden tools + action fragments
│ agent_guardrails  │  risk tier, secrets, sandbox, watermarks
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ MCP / CLI runtime │  no send/file/pay tools exist
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Company memory    │  path sandbox + audit.jsonl
└───────────────────┘
```

## Specialist risk map

| Skill | Default risk | HITL |
|-------|--------------|------|
| market-validator | low–medium | sources required |
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

- `harden_status` — policy snapshot  
- `harden_check` — classify an action  

## Related

- `compliance/hitl-matrix.md`  
- `COMPLIANCE.md`  
- Aether `guardrails.py` / `COMPLIANCE.md`  
