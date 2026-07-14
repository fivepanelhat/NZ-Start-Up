# Status dashboard + board pack (v0.8)

## Status

```bash
nz-startup status my-startup
nz-startup status my-startup --json
```

Writes:

- `status/status-latest.md`
- `status/status-latest.json`

Score bands: **early** (<50) · **progressing** (50–79) · **ready** (80+).

Informational only — does not certify compliance.

## Board / mentor pack

```bash
nz-startup board pack my-startup
# optional: --no-refresh to skip regenerating weekly/status
```

Writes:

- `board-packs/board-pack-latest.zip`
- Includes profile, pipeline, calendar, grants, weekly, status, demo report, digests

**Different from** `handoff pack` (accountant finance dump).

## Smoke

```bash
nz-startup smoke
# exit code 0 = pass
```

Runs isolated sample path: init → pipeline → bank → xero → invoice → weekly → status → handoff → board → cohort pack → demo quick.

## Sales one-pager

`templates/sales-one-pager.md` — copy for EDA conversations.
