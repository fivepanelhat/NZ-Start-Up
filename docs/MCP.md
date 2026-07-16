# MCP Connectors (v0.2)

Local **stdio** MCP server with hard HITL ceilings.

## Install

```bash
pip install -e ".[mcp]"
# or
pip install -e ".[all]"
```

## Run

```bash
nz-startup mcp
# equivalent:
python -m nz_startup mcp
```

Wire into Claude Desktop / Cursor / other hosts via the single **`mcp.json`** in this repo root
(G13: do not maintain a parallel `.mcp.json` - drift risk).

**Paths:** env uses relative `NZ_STARTUP_ROOT=.` and `NZ_STARTUP_MEMORY=./memory`.
Set absolute paths in your client if it does not resolve cwd to the repo root.
VS Code `${workspaceFolder}` is **not** expanded by all MCP hosts.

**Annotations:** the entire tool surface is non-destructive (reads + local drafts only).
Clients may treat tools as `readOnlyHint` / `destructiveHint: false` for auto-approval UX.

## Tools (allowed)

| Tool | Purpose |
|------|---------|
| `list_companies` | List company memory IDs |
| `init_company_memory` | Scaffold local memory (+ pipeline/calendar/grants) |
| `read_company_file` / `write_company_file` | Memory I/O (audited) |
| `append_company_decision` | Decision log |
| `append_rdti_log` / `list_rdti_log` | Contemporaneous RDTI logging |
| `generate_weekly_operating_review` | Board pack with live pipeline/calendar/grants |
| `save_outreach_draft` | CRM-style draft only - **never sends** |
| `save_legal_draft` | Watermarked legal draft |
| `nzbn_lookup` | Read-only NZBN/name (offline without API key) |
| `pipeline_list` / `pipeline_add` / `pipeline_update` / `pipeline_summary` | Local CRM stages |
| `calendar_list` / `calendar_add` / `calendar_update` / `calendar_reminders` | Deadlines |
| `grants_list` / `grants_add` / `grants_update` / `grants_rank` | Grant tracker CSV |
| `xero_status` / `xero_snapshot` | Xero **read-only** finance snapshot |
| `export_deadline_reminders` | ICS + digest files (never emails) |
| `bank_import_csv` / `bank_triage` | Bank CSV import + category triage |
| `gst_prepare_worksheet` | GST **working papers** only (not a filing) |
| `invoice_triage_path` / `invoice_list` | Invoice field extraction + registry |
| `handoff_pack_create` | Local accountant zip (never emails) |
| `cohort_list` / `cohort_status` / `cohort_pack` | White-label cohorts (no email) |
| `demo_run` | EDA demo walkthrough report |
| `company_status` | Readiness score + gaps |
| `board_pack_create` | Mentor/board zip (not accountant) |
| `smoke_run` | Local e2e smoke |
| `onboard_company` | First-hour founder wizard |
| `pilot_offer_create` | Paid pilot pack (DRAFT_NOT_SENT) |
| `cohort_partner_report` | EDA seat readiness report |
| `hitl_policy_summary` / `check_hitl_action` | Policy helpers |

## Tools deliberately absent

`send_email`, `file_companies_office`, `file_ird`, `move_money`, `submit_grant`, `sign_document`, `realme_login`, ...

## NZBN API

Set `BUSINESS_GOVT_API_KEY` (or `NZBN_API_KEY`) for live read-only calls to the business.govt.nz gateway. Without a key, `nzbn_lookup` returns offline human-action guidance and **does not invent NZBNs**.

## Security notes

- Company memory is local by default (`memory/companies/`).
- Runtime company data is gitignored.
- Never store IRD numbers, bank credentials, or API keys in memory files.
