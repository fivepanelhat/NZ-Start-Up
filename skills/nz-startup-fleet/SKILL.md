---
name: nz-startup-fleet
version: "0.1.0"
model_tier: standard
type: orchestration
requires_hitl: true
cultural_sensitivity: high
description: >
  Product entry skill for NZ Start-Up in a Box. Bootstraps company memory, explains the fleet, and starts dogfooding with CAT standards and HITL compliance.
metadata:
  status: active
  owner: Coastal Alpine Tech
  stage: pre-seed
  product: nz-startup-in-a-box
  standards: [gold, diamond, platinum]
  rd_start: "2025-08-08"
  founding_date: "2026-08-08"
  last_updated: "2026-07-15"
tags:
  - fleet
  - bootstrap
  - product
  - nz-startup
---

# NZ Start-Up Fleet

## Overview
Meta skill for the product. Use when the user installs the pack or says
"run my NZ startup agents" / "startup in a box".

## Bootstrap sequence
1. Load `agent-hardening` then `cat-architectural-standards` — ceilings + Gold/Platinum/Diamond.
2. Ensure company memory exists (copy example structure).
3. Introduce the 10 digital employees and autonomy slogan.
4. Offer one of: formation pack | weekly board | RDTI log start | GTM draft week | `demo run`.
5. For EDA partners: `cohort init` + `cohort pack` white-label path.
6. Remind hard boundaries (file/send/pay = human). Run `nz-startup harden status` if needed.

## Dogfood mode (Coastal Alpine Tech pre-seed)
- Company: Coastal Alpine Tech Limited · Taranaki · founded 8 Aug 2026 · R&D since 8 Aug 2025
- Founding context: Wayne Roberts · Taranaki whānau · six generations in agriculture
- Map 30/60/90 plan actions to fleet skills
- Prefer paid pilot pipeline discipline over new product forks
- Weekly board report + `nz-startup demo run` is the EDA white-label conversation
- Dual licence: keep proprietary Track A default; sell Track B commercial rights
- See `ABOUT.md`, `docs/DUAL_LICENCE.md`, `docs/WHITE_LABEL.md`, `docs/DEMO.md`

## Guardrails
- Do not promise autonomous company operation
- Do not skip compliance docs on first run

## References
- `README.md`
- `docs/GETTING_STARTED.md`
- `docs/FLEET.md`
