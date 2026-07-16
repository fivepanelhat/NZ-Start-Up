# Onboard, pilot offers, partner reports (v0.9)

## Founder onboard

```bash
nz-startup onboard my-startup \
 --legal-name "Example Labs Limited" \
 --wedge "Sovereign edge AI for operators" \
 --icp "Regional councils and co-ops"
```

Creates/updates company memory, seeds pipeline/calendar/grants, writes:

- `onboard/30-day-plan.md`
- weekly board + status

## Paid pilot offer

```bash
nz-startup pilot offer my-startup \
 --customer "Taranaki Regional Council" \
 --fee 1500 \
 --days 90 \
 --champion "Name" \
 --criteria "Weekly champion check-ins; offline demo accepted; go/no-go on conversion"
```

Writes under `commercial/pilots/`:

- offer markdown + JSON
- agreement outline (not legal advice)
- `pilot-offer-latest.zip`

**DRAFT_NOT_SENT** - human emails and signs.

## Cohort partner report

```bash
nz-startup cohort report vt-powerup
nz-startup cohort report vt-powerup --anonymise
```

Seat readiness scores for EDA ops. Manual delivery only.
