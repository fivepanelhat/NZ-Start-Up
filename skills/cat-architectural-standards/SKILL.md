---
name: cat-architectural-standards
version: "1.0.0"
model_tier: light
type: orchestration
requires_hitl: true
cultural_sensitivity: high
description: >
  Classify and govern NZ Start-Up in a Box work under CAT Gold, Diamond, and Platinum standards. Use for planning, reviews, HITL gates, and maturity checks.
metadata:
  status: active
  owner: Coastal Alpine Tech
  product: nz-startup-in-a-box
  standards: [gold, diamond, platinum]
  last_updated: "2026-07-14"
tags:
  - cat
  - gold
  - diamond
  - platinum
  - governance
---

# CAT Architectural Standards

## Overview
Top-level governance skill for Coastal Alpine Tech and NZ Start-Up in a Box.
Operationalises Gold (workflow), Diamond (foundation), and Platinum (intelligence flywheel).

## When to Use
- Starting any non-trivial planning or architecture session
- Reviewing whether work claims a maturity tier honestly
- Before release or white-label packaging

## Instructions

### 1. Classify
State primary and secondary tier:
- **Gold** — founder lifecycle / process mapping / templates
- **Diamond** — CI, security, privacy, production hygiene
- **Platinum** — memory, agents, flywheel, learning loops

### 2. Apply tier rules
- Gold → linear phase gates; map to real NZ founder steps
- Diamond → security, validation, audit, no secrets
- Platinum → capture points, company memory writes, evaluation

### 3. HITL
Load `compliance/hitl-matrix.md`. Block forbidden autonomies.

### 4. Cultural overlay
Load `compliance/te-mana-raraunga.md` for all tiers.

## Guardrails
- Never claim Diamond without CI/security evidence
- Never treat Platinum as "add more AI" without Gold workflow
- HITL for cultural, health, funding pathway claims

## Output
```markdown
## Classification
- Primary: Gold|Diamond|Platinum
- Secondary: ...
- HITL required: yes/no
- Cultural review: yes/no
- Proceed: ...
```

## References
- `docs/STANDARDS.md`
- `standards/*.md`
- `references/CHANGELOG.md`
