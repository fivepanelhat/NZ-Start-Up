# NZ Start-Up in a Box

**v1.0 — Local founder OS + white-label EDA kit for New Zealand**  
Formation through funding, with hard legal ceilings and CAT Gold / Diamond / Platinum Aether standards.

> **One download.** Skills + NZ knowledge + templates + HITL compliance + localhost console.  
> **Built on [Aether](https://github.com/fivepanelhat/Aether).**  
> **Coastal Alpine Tech Limited** · Taranaki · Aotearoa New Zealand.

## What you get

A **small orchestrator + skills-heavy specialist fleet** (not 30 fake “autonomous employees”):

| # | Digital employee | Role | Autonomy ceiling |
|---|------------------|------|------------------|
| 1 | Formation Officer | Name, constitution pack, IRD/GST prep, NZBN | Prepares; founder files via RealMe |
| 2 | Compliance Registrar | Annual returns, Privacy Act, H&S, employment checklists | Drafts + calendar; never self-certifies |
| 3 | Grants & RDTI Clerk | Grant radar, eligibility, R&D activity logging | High autonomy on logs; human submits apps |
| 4 | Market Validator | Sizing, comps, interview guides | Research autonomous; sources + confidence |
| 5 | GTM / Pipeline Rep | ICP, outreach drafts, CRM hygiene, proposals | **Sends nothing** without approval (UEM Act) |
| 6 | Content & Comms Officer | One-asset-five-outputs engine | Schedules only pre-approved content |
| 7 | Finance Clerk | Bookkeeping triage, GST prep, runway alerts | Never moves money; not a tax agent |
| 8 | Funding Analyst | Investor targeting, data room, SAFE comparison | Prep only; FMCA advice boundary |
| 9 | Legal Document Assistant | NDA, pilot, ToS, employment drafts | Watermarked “not legal advice” |
| 10 | Board / Chief-of-Staff | Weekly ops review, routing, company memory | Escalates; never decides |

The **NZ moat** is jurisdiction depth (Companies Office, IRD, RDTI, regional grants, Te Mana Raraunga) — not agent novelty.

## Standards (mandatory)

Every piece of work is classified under **CAT Architectural Standards**:

| Tier | Name | Meaning for this product |
|------|------|--------------------------|
| **Gold** | Workflow-native design | Fleet maps the real NZ founder lifecycle end-to-end |
| **Diamond** | Enterprise-grade foundation | CI, skill validation, security, audit logs, privacy defaults |
| **Platinum** | Self-improving intelligence | Company memory + RDTI/build logs feed a data flywheel |

Load `skills/cat-architectural-standards` before planning significant work. See `docs/STANDARDS.md`.

## Hard boundaries (where products die)

Agents may **inform, draft, prepare, monitor, and remind**.  
Humans must **advise, sign, file, send, and pay**.

Specifically:

- No legal advice (Lawyers and Conveyancers Act 2006)
- No regulated financial advice (FMC Act)
- No tax-agent behaviour
- No autonomous outbound email (Unsolicited Electronic Messages Act 2007)
- No Companies Office / IRD filing except via founder-authenticated action
- Privacy Act 2020 + Te Mana Raraunga for any hosted founder data
- Visible audit trail for agent actions

## Quick start

### One-command install (Windows)

```powershell
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
powershell -ExecutionPolicy Bypass -File .\install.ps1
nz-startup doctor
nz-startup onboard my-startup --legal-name "My Labs Limited"
nz-startup console --port 8765
# open http://127.0.0.1:8765/
```

### Option A — With Aether (recommended)

```powershell
# After install.ps1 / install.sh, skills are copied to ~/.aether/skills
# Or:
nz-startup install-skills --mode copy
```

Then ask your Aether / Claude / agent runner:

```text
Load cat-architectural-standards and board-chief-of-staff.
Initialise company memory for my startup and run a weekly operating review.
```

### Option B — MCP connectors (v0.2)

```powershell
python -m pip install -e ".[mcp]"
nz-startup mcp
```

Host config sample: `mcp.json`. Tools are **drafts-only** — no send/file/pay. See `docs/MCP.md`.

### Option C — Claude Code / Cowork plugin-style

Copy `skills/*` into your skills directory. Each skill is a self-contained `SKILL.md` pack with references and templates.

### CLI cheat sheet

```powershell
nz-startup init my-startup
nz-startup rdti add my-startup --hours 2 --activity "..." --uncertainty "..." --evidence "commit:abc"
nz-startup pipeline add my-startup --account "TRC" --stage discovery --next-step "book demo"
nz-startup pipeline update my-startup P001 --stage pilot
nz-startup calendar add my-startup --item "GST prep" --due 2026-08-28 --category finance
nz-startup calendar remind my-startup --days 14
nz-startup grants rank my-startup
nz-startup xero snapshot my-startup --offline
nz-startup bank import my-startup --file templates/bank-feed-sample.csv
nz-startup bank triage my-startup
nz-startup gst prepare my-startup --start 2026-07-01 --end 2026-07-31
nz-startup invoice triage my-startup --path templates/sample-tax-invoice.txt
nz-startup handoff pack my-startup
nz-startup cohort init vt-powerup --partner "Venture Taranaki" --programme "PowerUp"
nz-startup cohort pack vt-powerup
nz-startup demo run --company demo-eda --partner "Venture Taranaki"
nz-startup onboard my-startup --legal-name "Example Labs Limited" --wedge "…" --icp "…"
nz-startup pilot offer my-startup --customer "Named Account" --fee 1500
nz-startup cohort report vt-powerup --anonymise
nz-startup status demo-eda
nz-startup board pack demo-eda
nz-startup smoke
nz-startup doctor
nz-startup console --port 8765
nz-startup export reminders my-startup --days 14
nz-startup draft-outreach my-startup --subject "Intro" --body "..."
nz-startup nzbn "Example Limited"
nz-startup weekly my-startup
nz-startup validate
```

### Validate skills

```powershell
python -m pip install -e ".[dev]"
python scripts/validate_skills.py
pytest -q
```

## Repository layout

```text
skills/                 # Aether-compatible digital employees + CAT standards
knowledge/              # NZ integrations, funding landscape, lifecycle map
templates/              # Checklists and draft outlines (not formal legal docs)
compliance/             # HITL matrix, Privacy Act, Te Mana Raraunga, legal boundaries
standards/              # Gold / Diamond / Platinum operational definitions
memory/                 # Company memory schema + example (runtime data gitignored)
docs/                   # Architecture, fleet, getting started
scripts/                # Skill validators
tests/                  # CI smoke tests
.github/workflows/      # Skills CI
```

## Pricing posture (product, not this open pack)

Reference tiers for a commercial wrap (token burn is real — default agents to on-demand + weekly cadence):

| Tier | Indicative | Who |
|------|------------|-----|
| Founder | ~NZ$49/mo | Solo founder |
| Active | ~NZ$149/mo | Active pipeline |
| Accelerator cohort | ~NZ$399 seat | EDA / incubator white-label |
| White-label | per-seat | Venture Taranaki / RBP network style |

This repo is the **open skills core**. White-label packaging is a separate commercial layer.

## Compliance & culture

- `COMPLIANCE.md` — product compliance framework
- `compliance/*` — operational matrices
- Te Tiriti / Te Mana Raraunga as architectural constraints, not marketing

## Roadmap

1. **v0.1–0.9** — Skills → finance → white-label → commercial pilot kits  
2. **v1.0 (now)** — Local product release: doctor + localhost Founder Console  
3. **Native desktop shell** — only after paid demand  
4. **Hosted SaaS** — only with funding + team (not solo)

## Related

- [Aether](https://github.com/fivepanelhat/Aether) — sovereign agentic orchestrator
- [fivepanelhat](https://github.com/fivepanelhat/fivepanelhat) — Kiwi Edge portfolio map
- Design reference: Agent Fleet Design (July 2026)

## Disclaimer

**Not legal, financial, tax, or cultural advice.** Confirm application of NZ statutes with a qualified professional before relying on any draft or checklist. Templates are educational outlines only.

## License

Apache-2.0 — see `LICENSE` and `NOTICE`.
