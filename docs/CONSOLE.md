# Founder Console (v1.0)

Localhost-only web UI over company memory.

```bash
nz-startup console --port 8765
# http://127.0.0.1:8765/
```

## Features

- List companies  
- Status score + checks  
- Generate weekly board / refresh status  

## Hard limits

- Binds **only** to `127.0.0.1` / localhost (non-local bind refused)  
- No email, no IRD/Companies Office filing, no payments  
- Board/handoff/pilot packs remain CLI (smaller attack surface)  

## Not SaaS

This is not multi-tenant hosting. Founder data stays in local `memory/companies/`.
