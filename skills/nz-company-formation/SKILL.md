---
name: nz-company-formation
description: Use when preparing or executing NZ company registration and post-incorporation setup. Handles Companies Office name reservation, constitution and share structure options, IRD/GST registration prep, NZBN, business bank account requirements, and first compliance calendar. Always requires founder to file via their own RealMe session. Trigger phrases include incorporate, register company, Companies Office, name reservation, GST registration, pre-incorporation checklist, incorporation pack, Day 0.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-20"
  related: formation-officer, venture-taranaki-engagement, aether-hitl-protocol, cat-architectural-standards
---

# NZ Company Formation

Production skill for the full NZ limited company formation and Day-0 readiness sequence. Designed for solopreneur deep-tech founders (especially Coastal Alpine Tech style) who need clean, audit-ready incorporation aligned with Venture Taranaki, RDTI, and future investment pathways.

## Core Rules (Non-Negotiable)

- **Founder files everything.** This skill prepares packs, checklists, and draft documents only. Never attempt to complete RealMe authentication, pay fees, or submit forms on the founder’s behalf.
- All outputs must begin with the standard draft header and end with an explicit **Human Action Checklist**.
- Information only — not legal, tax, or financial advice. Flag any constitution or share-structure recommendations for lawyer review.
- Prefer 100% founder-owned with a documented 10–15% ESOP-shaped gap in thinking for a future technical hire (do not create the ESOP yet).

## When to Load

- Pre-incorporation planning (now → 8 August 2026 for Coastal Alpine Tech)
- Name reservation and structure decisions
- Incorporation day and same-week post-incorporation setup (bank, IRD, GST, Xero, insurance)
- Any request that touches Companies Office, NZBN, or first compliance calendar

## Standard Workflow

1. **Confirm context**
   - Read company memory / profile if it exists.
   - Confirm intended incorporation date, location (Taranaki preferred), and share structure intent.
   - Note any Venture Taranaki / PowerUp Investment Month timing constraints.

2. **Produce the Incorporation Pack** (create or update under `incorporation-pack/`)
   - `name-options.md` — 3–5 name options with rationale; note that availability must be verified live on Companies Office.
   - `structure-options.md` — recommended share structure (100% founder + ESOP thinking note), director details, constitution approach (standard vs tailored).
   - `checklist.md` — full pre- and post-incorporation checklist timed to the target date.
   - `ird-gst-prep.md` — IRD number application steps, GST registration decision criteria (register if pilots will invoice at >$60k/yr pace), NZBN.
   - `bank-and-insurance.md` — business bank account requirements list + public liability insurance quote checklist (critical when placing hardware on farms).

3. **Day-0 same-week sequence** (for the actual incorporation week)
   - Incorporate
   - Open business bank account
   - IRD number + GST registration
   - Xero (or free equivalent) setup
   - Business insurance quote
   - Tag v0.1 release on GitHub if product exists

4. **First compliance calendar**
   - Annual return reminder
   - RDTI activity log start date
   - Any sector-specific obligations (Privacy Act, HSWA if hardware is involved)

## Venture Taranaki Alignment

- Aim to complete name reservation and incorporation so the company launches **inside** a PowerUp Investment Month window when possible.
- After incorporation, immediately prepare the ScaleUp grant application materials ($5k for demo hardware + enclosure certification).
- Flag readiness for Enterprise Advisor conversation and RBP Capability Development Fund voucher eligibility (GST registered + commercially trading).

## Guardrails & HITL

- Never state a name is “available” — only “appears available based on last check; must be verified and reserved on Companies Office”.
- Never draft or send any communication that implies legal advice on constitution wording.
- All external filings and payments require explicit founder action in their own authenticated session.
- Output every pack with:

```markdown
# DRAFT – NOT FOR SUBMISSION
Skill: nz-company-formation
HITL: Founder must file in own RealMe-authenticated session
Not legal or tax advice
```

## Success Criteria

- Pack is complete, dated, and contains only actionable items the founder can execute.
- Human Action Checklist is clear and prioritised.
- Timing notes reference current Venture Taranaki programmes where relevant.
- No unsubstantiated claims about name availability or tax treatment.

## References

- Existing `formation-officer` skill (lighter companion)
- Companies Office: companies-register.companiesoffice.govt.nz
- IRD / myIR guidance
- NZBN
- Coastal Alpine Tech 30/60/90 Day Solopreneur Plan (Day 0 = 8 August 2026)
