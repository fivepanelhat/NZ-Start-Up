---
name: agent-hardening
version: "1.0.0"
type: security
requires_hitl: true
cultural_sensitivity: high
description: >
  Enforce NZ Start-Up agent autonomy ceilings, secret refusal, path sandboxing,
  watermarks, and HITL for high-risk domains. Load before any multi-skill fleet work.
metadata:
  status: active
  owner: Coastal Alpine Tech
  product: nz-startup-in-a-box
  standards: [gold, diamond, platinum]
  last_updated: "2026-07-14"
tags:
  - security
  - hitl
  - guardrails
  - compliance
---

# Agent Hardening

## Overview
Cross-cutting security skill for the NZ Start-Up fleet. Operationalises autonomy ceilings
aligned with CAT Gold/Diamond/Platinum and Aether COMPLIANCE.

## When to Use
- Starting any fleet session (`nz-startup-fleet`, board routing)
- Before legal, finance, GTM send, grants submit, or cultural content
- When reviewing agent outputs for shipment or customer delivery
- After adding new skills or MCP tools

## Instructions

### 1. Load policy
Restate: agents **inform, draft, prepare, monitor, remind**; humans **advise, sign, file, send, pay**.

### 2. Classify risk
- **Low** — research notes, internal formatting
- **Medium** — pipeline updates, calendar, content drafts
- **High** — legal drafts, GST/bank, outreach, grants, funding
- **Critical** — anything resembling file/send/pay/sign or cultural extraction

High and critical → HITL before human acts on the artefact.

### 3. Sandbox
- Writes only under `memory/companies/<id>/`
- No `..` path traversal
- Refuse secrets (PEM, API keys, JWT, connection strings)

### 4. Watermark outputs
Apply as needed: `DRAFT`, `NOT LEGAL ADVICE`, `NOT FINANCIAL ADVICE`,
`INFORMATION ONLY`, `DRAFT_NOT_SENT`, `PREPARED BY AGENT`.

### 5. Cultural safety
Te Mana Raraunga / Te Tiriti: no invented iwi endorsement; escalate whenua-linked data designs.

### 6. Runtime
Prefer CLI/MCP tools that already enforce HITL. Never invent tools named send_/file_/pay_.

## Guardrails
- `requires_hitl: true` for this skill when changing policy
- Do not weaken ceilings to "make demos cooler"
- Confirm statute application with NZ counsel for commercial claims

## References
- `compliance/hitl-matrix.md`
- `docs/AGENT_HARDENING.md`
- `nz_startup/agent_guardrails.py`
- `nz_startup/hitl.py`
- CAT skill: `cat-architectural-standards`
