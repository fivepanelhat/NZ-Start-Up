# Founder Console

Localhost-only web UI over company memory.

```bash
nz-startup console --port 8765 --open
# or with fixed token:
nz-startup console --token "$env:NZ_STARTUP_CONSOLE_TOKEN" --open
# or:
nz-startup desktop   # pywebview if installed: pip install '.[desktop]'
```

## Features

- List companies with status scores  
- Company page: pipeline, grants, 14d reminders, weekly excerpt  
- Actions: refresh status, weekly board, board pack zip, export reminders  
- Local artefact path table  

## Hard limits

- Binds **only** to `127.0.0.1` / localhost (non-local bind refused)  
- **G11 session token** — auto-minted at start (printed + embedded in open URL).
  Also accepted via `Authorization: Bearer`, `X-NZ-Startup-Token`, or cookie.
  Set `NZ_STARTUP_CONSOLE_TOKEN` to pin a stable secret.  
- No email, no IRD/Companies Office filing, no payments  
- Pilot send / outreach send remain human CLI paths  

## Not SaaS

This is not multi-tenant hosting. Founder data stays in local `memory/companies/`.
