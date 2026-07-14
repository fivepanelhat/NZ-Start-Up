# Reminder exports (v0.4)

## ICS

Importable into Google Calendar, Outlook, Apple Calendar:

```bash
nz-startup export ics my-startup --days 90
# or full pack:
nz-startup export reminders my-startup --days 14 --ics-days 90
```

Files:

- `exports/deadlines-YYYY-MM-DD.ics`
- `exports/deadlines-latest.ics`

## Markdown digest

Human-readable board/email **paste** source (agent does **not** send email):

```bash
nz-startup export digest my-startup --days 14
```

- `exports/deadline-digest-YYYY-MM-DD.md`
- `exports/deadline-digest-latest.md`

## Weekly board

`nz-startup weekly` auto-refreshes `deadlines-latest.ics` and `deadline-digest-latest.md`.
