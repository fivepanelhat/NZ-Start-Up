# NZ Start-Up in a Box — v1.6.0

**Coastal Alpine Tech Limited — Pre-seed** · Taranaki · Aotearoa New Zealand  
**R&D since 8 August 2025** · **Founded 8 August 2026**  
**Local founder OS + white-label EDA kit** · dual proprietary/commercial licence  
Built with **CAT Gold / Diamond / Platinum** on **Aether**  
Dev tools: **Grok 4.5 Build** · **Claude Pro Code** · **Claude Computer Use** · **Google Gemini 3.5 Flash**

## What 1.6 means

Trust-transfer layer (Claude T1–T9) on the v1.5 fleet ops base:

| Ops | Command |
|-----|---------|
| Deterministic evals | `nz-startup eval --write` |
| Live/rubric evals | `nz-startup eval --live` |
| Weekly cadence | `nz-startup schedule install` / `verify` / `run` |
| Task state | `nz-startup tasks add\|list\|update` |
| Memory INDEX | `nz-startup index write\|compact` |
| Token budget + hard cap | `nz-startup budget set --enforce` |
| Skills pack + SHA256/SBOM | `nz-startup pack` |
| Encrypted backup | `nz-startup backup create <co> --passphrase …` |
| Audit OTel export | `nz-startup audit export <co>` |
| Standards mapping | `compliance/standards-mapping.md` |
| Console auth | session token (`hmac.compare_digest`) |

## What 1.5 means

Fleet **ops layer** on top of hardened guardrails (gap analysis G1–G14):

| Ops | Command |
|-----|---------|
| Golden evals | `nz-startup eval --write` |
| Weekly cadence | `nz-startup schedule install` / `run` |
| Task state | `nz-startup tasks add\|list\|update` |
| Memory INDEX | `nz-startup index write\|compact` |
| Token budget | `nz-startup budget show\|set\|record` |
| Skills pack zip | `nz-startup pack` |
| Console auth | auto session token on `console` |

## What 1.x means

The **production local product** (skills + CLI + MCP + localhost console + desktop-lite):

| Included | Deferred |
|----------|----------|
| 13 digital-employee skills + CAT standards | Multi-tenant hosted SaaS |
| Full finance/ops loop (bank, GST papers, invoices, handoff) | Always-on autonomous agents |
| White-label cohorts + EDA demo | Unsolicited email / IRD filing automation |
| Status, board pack, pilot offers, partner reports | Full packaged native installers |
| **Founder Console** + **desktop-lite** (`pywebview` optional) | Cloud data hosting of founder secrets |
| Evals · quarantine · allow-list HITL · freshness · telemetry · scheduler | RealMe / myIR computer-use (G15 watch) |

Full native packaged desktop remains demand-gated; desktop-lite covers day-to-day local UI.

## Install

```bash
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
pip install -e ".[all]"
nz-startup doctor
nz-startup smoke
nz-startup install-skills
```

Windows: `powershell -ExecutionPolicy Bypass -File .\install.ps1`

## First hour

```bash
nz-startup onboard my-startup --legal-name "…" --wedge "…" --icp "…"
nz-startup console --port 8765 --open
# or: nz-startup desktop
```

## EDA demo

```bash
nz-startup demo run --partner "Venture Taranaki"
nz-startup board pack demo-eda
nz-startup cohort pack <cohort-id>
```

## Autonomy slogan

> Agents inform, draft, prepare, monitor, and remind.  
> Humans advise, sign, file, send, and pay.

## Licence

**Dual licence** — Track A proprietary (`LICENSE`) + Track B commercial (`LICENSE-COMMERCIAL.md`).  
Copyright under NZ law (Copyright Act 1994). Not open source.  
See `docs/DUAL_LICENCE.md` and `ABOUT.md`.

## Support

Issues: https://github.com/fivepanelhat/NZ-Start-Up/issues  
Coastal Alpine Tech · Taranaki · Aotearoa New Zealand
