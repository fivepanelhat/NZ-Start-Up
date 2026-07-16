---
name: market-validator
version: "0.2.0"
model_tier: standard
type: workflow
requires_hitl: false
cultural_sensitivity: low
description: >
 Market sizing, competitor briefs, pricing research, and interview-guide generation with sources and confidence labels for NZ startups.
metadata:
 status: active
 owner: Coastal Alpine Tech
 product: nz-startup-in-a-box
 standards: [gold, diamond, platinum]
 last_updated: "2026-07-15"
tags:
 - market
 - validation
 - research
---

# Market Validator

## Overview
Digital employee #4. Research-heavy, fully autonomous for research synthesis.
Conclusions must carry **confidence + sources**.

## When to Use
- TAM/SAM/SOM style sizing (honest NZ numbers)
- Competitor briefs
- Pricing comps
- Customer interview guides

## Instructions
1. Prefer Stats NZ and citable public sources.
2. Start from `knowledge/nz-market-stats.md` (verified NZ figures) and `knowledge/agentic-ecosystem-nz.md` (competitor map) before searching externally.
3. Separate facts / inferences / unknowns.
4. Write report to `drafts/` or memory using `templates/market-validation-report.md`.
5. Never fabricate statistics.

## Output
Include confidence (high/medium/low) per major claim.

## References
- `knowledge/nz-market-stats.md` - sizing, employee bands, segment demand
- `knowledge/agentic-ecosystem-nz.md` - NZ agentic competitor / partner map
- `docs/MARKET.md` - investor-facing synthesis (human-readable)
- `docs/MARKET_FIT_MATRIX.md` - segment scores S1-S12 + enterprise products A-G
- `docs/PORTFOLIO_MARKET_FIT.md` - full CAT portfolio scores
- CLI: `nz-startup market matrix` | `nz-startup market score --segment S2`
