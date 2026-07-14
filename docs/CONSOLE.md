# Founder Console (v1.1)

Localhost-only web UI over company memory.

```bash
nz-startup console --port 8765 --open
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
- No email, no IRD/Companies Office filing, no payments  
- Pilot send / outreach send remain human CLI paths  

## Not SaaS

This is not multi-tenant hosting. Founder data stays in local `memory/companies/`.
