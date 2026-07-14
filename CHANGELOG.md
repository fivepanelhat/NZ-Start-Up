# Changelog

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
