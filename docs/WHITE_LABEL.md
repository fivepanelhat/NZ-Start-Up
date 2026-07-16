# White-label cohorts (v0.7)

For **EDAs, accelerators, incubators, accounting firms** - sell per-seat / per-cohort capacity without multi-tenant SaaS.

**Ready-to-use approach kit (Venture Taranaki PowerUp):** [`docs/VT_POWERUP_APPROACH.md`](./VT_POWERUP_APPROACH.md) - one-pager, verified 10-minute demo runbook, DRAFT_NOT_SENT outreach email, objection crib sheet, follow-through sequence.

## Thesis

> "Nick, but scalable" - white-label fleet on infrastructure you already run, 
> not a new company. Seat data stays local; legal ceilings stay on.

## Commands

```bash
# Create cohort + brand overlay
nz-startup cohort init vt-powerup \
 --partner "Venture Taranaki" \
 --programme "PowerUp" \
 --quota 15 \
 --tagline "Founder OS for Taranaki"

# Add a founder seat (creates company memory)
nz-startup cohort add-seat vt-powerup --founder alice --company alice-labs --name "Alice"

# List
nz-startup cohort list
nz-startup cohort list vt-powerup

# Partner readiness report (optional anonymise)
nz-startup cohort report vt-powerup
nz-startup cohort report vt-powerup --anonymise

# White-label zip for partner (NO seat PII)
nz-startup cohort pack vt-powerup
# -> cohorts/vt-powerup/exports/white-label-latest.zip
```

## Layout

```text
cohorts/<id>/
 cohort.json # config + seats (local ops)
 brand/ # BRAND.md, welcome.md
 PARTNER_README.md
 seats/<founder>/ # seat.json, WELCOME.md
 exports/ # white-label zips
```

## What the pack contains

- Brand + founder welcome
- Partner ops readme
- MCP sample
- Skills inventory + install path
- `cohort.json` **without seats array**

## What it does not do

- Host multi-tenant founder data
- Email partners or founders
- Lift HITL ceilings (still draft/prepare only)

## Packaging (conceptual tiers)

| Tier | Who it is for |
|------|---------------|
| Founder | Individual founder seat |
| Active | Higher-usage founder / small team |
| Accelerator seat | Per-seat for cohort programmes |
| White-label | Custom per-cohort / partner packaging |

Specific commercial terms are set per pilot or partnership and are not published as a fixed public price list. Contact for pilot terms.

Token burn is real — default on-demand + weekly cadence.
