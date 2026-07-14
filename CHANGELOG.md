# Changelog

## 1.2.0 — 2026-07-14

### Security / agents
- **Agent hardening plane**: `agent_guardrails.py`, skill `agent-hardening`
- Stronger HITL forbidden tools/fragments (bypass, mass mail, exfil)
- Memory writes: path sandbox + secret-pattern refusal
- CLI: `harden status|check|policy`
- MCP: `harden_status`, `harden_check`
- Docs: `docs/AGENT_HARDENING.md`

### Architecture
- Detailed architecture doc with diagrams: `docs/ARCHITECTURE_DETAILED.md`
- Ultra glassmorphism architecture hero: `assets/architecture-glassmorphism.jpg`

## 1.1.0 — 2026-07-14

### Added
- Console company view: pipeline, grants, 14d reminders, weekly excerpt, artefact paths
- Console actions: board pack zip + export reminders (local only)
- `nz-startup console --open` opens system browser
- `nz-startup desktop` desktop-lite (pywebview optional, else browser)
- Optional extra: `pip install '.[desktop]'`
- Home list shows status score per company
- Console security headers (nosniff, DENY frame)

## 1.0.0 — 2026-07-14

### Added
- **v1.0 local product release** — skills + CLI + MCP + localhost Founder Console
- `nz-startup console` — 127.0.0.1-only dashboard (status + weekly actions)
- `nz-startup doctor` — install/environment health checks
- `RELEASE.md`, `docs/CONSOLE.md`
- MCP: `doctor_run`
- Smoke includes doctor

### Notes
- Console refuses non-localhost binds (not multi-tenant SaaS)
- Full native desktop shell still demand-gated; console is the v1.0 UI surface

## 0.9.0 — 2026-07-14

### Added
- **Founder onboard wizard** (`onboard`) — profile, 30-day plan, seeds, weekly, status
- **Paid pilot offer pack** (`pilot offer`) — DRAFT_NOT_SENT commercial zip
- **Cohort partner report** (`cohort report`) — seat readiness, optional anonymise
- Demo walkthrough now includes **status + board pack**
- CLI/MCP for onboard, pilot, partner report
- Docs: `docs/PILOT_ONBOARD.md`

## 0.8.0 — 2026-07-14

### Added
- **Company status dashboard** (`status`) with readiness score, gaps, next actions
- **Board/mentor pack** zip (distinct from accountant handoff)
- **Smoke e2e** command for install/CI confidence
- Sales one-pager template for white-label pitch
- CLI: `status`, `board pack`, `smoke`
- MCP: `company_status`, `board_pack_create`, `smoke_run`
- Docs: `docs/STATUS_BOARD.md`

## 0.7.0 — 2026-07-14

### Added
- **White-label cohorts** for EDAs/accelerators: init, seats, brand overlay, pack zip (no seat PII)
- CLI: `nz-startup cohort init|add-seat|list|pack`
- MCP: `cohort_list`, `cohort_status`, `cohort_pack`
- **EDA demo walkthrough**: full + quick modes, demo report markdown
- CLI: `nz-startup demo run`
- MCP: `demo_run`
- Scripts: `scripts/demo_eda.ps1`, `scripts/demo_eda.sh`
- Docs: `docs/WHITE_LABEL.md`, `docs/DEMO.md`
- Template: `templates/cohort.example.json`

### Notes
- Still local-first; not multi-tenant SaaS
- White-label pack excludes founder seat PII

## 0.6.0 — 2026-07-14

### Added
- **Invoice triage** for PDF/text (optional `pypdf`): field extraction, confidence, registry
- CLI: `nz-startup invoice triage|list`
- MCP: `invoice_triage_path`, `invoice_list`
- **Accountant handoff pack** ZIP of working papers
- CLI: `nz-startup handoff pack`
- MCP: `handoff_pack_create`
- Sample: `templates/sample-tax-invoice.txt`
- Docs: `docs/INVOICES_HANDOFF.md`
- Optional extra: `pip install '.[pdf]'`

### HITL
- No auto GST claims; no emailing handoff packs
- Image invoices flagged for human OCR (no cloud OCR)

## 0.5.0 — 2026-07-14

### Added
- **Bank feed CSV import** with flexible headers, dedupe, category/GST-hint triage
- CLI: `nz-startup bank import|list|triage`
- MCP: `bank_import_csv`, `bank_triage`
- **GST worksheet assist** from bank period + Xero snapshot (working papers only)
- CLI: `nz-startup gst prepare --start --end`
- MCP: `gst_prepare_worksheet`
- Sample: `templates/bank-feed-sample.csv`
- Docs: `docs/BANK_GST.md`

### HITL
- No bank transfers, no myIR filing, no GST certification
- Estimates assume GST-inclusive bank amounts — human verifies tax invoices

## 0.4.0 — 2026-07-14

### Added
- **Xero read-only adapter** (`nz_startup/xero_readonly.py`): offline demo + live GET snapshot
- CLI: `nz-startup xero status|snapshot|refresh-token`
- MCP: `xero_status`, `xero_snapshot`
- Writes `finance/xero-snapshot.{json,md}` and runway note (no tokens stored)
- **Reminder exports**: ICS + markdown digest under `exports/`
- CLI: `nz-startup export reminders|ics|digest`
- MCP: `export_deadline_reminders`
- Weekly board auto-refreshes latest ICS/digest
- Docs: `docs/XERO.md`, `docs/EXPORTS.md`

### HITL
- No Xero write APIs; no emailing digests
- Forbidden tool names extended: `create_payment`, `email_digest`, etc.

## 0.3.0 — 2026-07-14

### Added
- **Pipeline CRM-lite** (`pipeline.csv` + markdown sync): stages lead→won/lost, add/update/list/summary
- **Calendar** (`calendar.csv`): deadlines, overdue/upcoming reminders (default 14 days)
- **Grants tracker** (`grants-tracker.csv`): add/update/list/rank by fit; NZ starter seed
- CLI: `nz-startup pipeline|calendar|grants ...`
- MCP tools for pipeline, calendar reminders, grants rank/update
- Weekly board review injects live pipeline + reminders + top grants
- Company `init` seeds all three trackers
- Templates: `templates/pipeline.csv`, `calendar.csv`, `grants-tracker.csv`

### HITL
- Pipeline never sends outreach
- Calendar never files compliance
- Grants never submits applications (`submitted` status flags human confirmation)

## 0.2.0 — 2026-07-14

### Added
- Python package `nz_startup` with CLI (`nz-startup`)
- Company memory init / read / write / decisions
- Contemporaneous RDTI log append + list
- Weekly operating review generator
- Outreach + legal draft writers (never send)
- Read-only NZBN lookup (offline without API key; live with `BUSINESS_GOVT_API_KEY`)
- HITL policy module and forbidden-tool inventory
- MCP stdio server (`nz-startup mcp`) — drafts-only CRM + NZBN read + memory + RDTI
- `install.ps1` / `install.sh` for Aether skills install
- `mcp.json` / `.mcp.json` host configs
- `docs/MCP.md`
- Runtime tests (`tests/test_runtime.py`)

### Standards
- Gold: founder lifecycle tooling
- Diamond: validated package, HITL enforcement in connectors
- Platinum: audit JSONL on memory/RDTI/draft writes

## 0.1.0 — 2026-07-14

- Initial skills pack (12 skills), compliance, templates, knowledge, CI
