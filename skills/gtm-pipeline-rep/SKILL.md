---
name: gtm-pipeline-rep
version: "0.2.0"
model_tier: standard
type: workflow
requires_hitl: true
cultural_sensitivity: low
description: >
 Build ICP lists, personalised outreach drafts, CRM hygiene notes, meeting prep, and proposals. Sends nothing without human approval under UEM Act constraints.
metadata:
 status: active
 owner: Coastal Alpine Tech
 product: nz-startup-in-a-box
 standards: [gold, diamond, platinum]
 last_updated: "2026-07-15"
tags:
 - gtm
 - pipeline
 - sales
 - uem
---

# GTM Pipeline Rep

## Overview
Digital employee #5. Drafts everything; **sends nothing** without approval.
NZ Unsolicited Electronic Messages Act 2007 makes autonomous cold email a legal risk.

## When to Use
- ICP list construction
- Outreach email drafts
- Meeting prep / follow-ups
- Pilot proposal generation from templates

## Instructions
1. Update `pipeline.md` stages.
2. Write drafts under `drafts/outreach/` with status `DRAFT_NOT_SENT`.
3. Provide human send checklist (consent, unsubscribe, accurate identity).
4. Never call send APIs.

## Guardrails
- UEM Act 2007
- No invented personal emails or phone numbers
- No fake social proof

## References
- `templates/outreach-draft.md`
- `compliance/hitl-matrix.md`
- `knowledge/nz-market-stats.md` - ICP employee bands + top-5 segments for list building
- `docs/MARKET.md` - ranked ICP priorities (P0 solo founders + EDA cohorts first)
