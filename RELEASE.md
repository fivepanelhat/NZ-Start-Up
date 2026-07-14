# NZ Start-Up in a Box — v1.1.0

**Local founder OS + white-label EDA kit** for Aotearoa New Zealand.  
Built with **CAT Gold / Diamond / Platinum** standards on **Aether**.

## What 1.x means

The **production local product** (skills + CLI + MCP + localhost console + desktop-lite):

| Included | Deferred |
|----------|----------|
| 12 digital-employee skills + CAT standards | Multi-tenant hosted SaaS |
| Full finance/ops loop (bank, GST papers, invoices, handoff) | Always-on autonomous agents |
| White-label cohorts + EDA demo | Unsolicited email / IRD filing automation |
| Status, board pack, pilot offers, partner reports | Full packaged native installers |
| **Founder Console** + **desktop-lite** (`pywebview` optional) | Cloud data hosting of founder secrets |

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

## License

**Proprietary** — Coastal Alpine Tech Limited. See `LICENSE` and `NOTICE`.  
Not open source. Commercial / white-label use requires a written licence.

## Support

Issues: https://github.com/fivepanelhat/NZ-Start-Up/issues  
Coastal Alpine Tech · Taranaki · Aotearoa New Zealand
