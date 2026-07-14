# Cohorts (white-label)

Runtime cohort configs and seats are created by:

```bash
nz-startup cohort init <id> --partner "Venture Taranaki"
nz-startup cohort add-seat <id> --founder alice --company alice-co
nz-startup cohort pack <id>
```

Seat company memories live under `memory/companies/` (gitignored).
White-label zips land in `cohorts/<id>/exports/` (gitignored).

See `docs/WHITE_LABEL.md`.
