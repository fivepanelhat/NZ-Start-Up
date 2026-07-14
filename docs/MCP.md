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

Wire into Claude Desktop / Cursor / other hosts via `mcp.json` in this repo.

## Tools (allowed)

| Tool | Purpose |
|------|---------|
| `list_companies` | List company memory IDs |
| `init_company_memory` | Scaffold local memory |
| `read_company_file` / `write_company_file` | Memory I/O (audited) |
| `append_company_decision` | Decision log |
| `append_rdti_log` / `list_rdti_log` | Contemporaneous RDTI logging |
| `generate_weekly_operating_review` | Board pack draft |
| `save_outreach_draft` | CRM-style draft only — **never sends** |
| `save_legal_draft` | Watermarked legal draft |
| `nzbn_lookup` | Read-only NZBN/name (offline without API key) |
| `hitl_policy_summary` / `check_hitl_action` | Policy helpers |

## Tools deliberately absent

`send_email`, `file_companies_office`, `file_ird`, `move_money`, `submit_grant`, `sign_document`, `realme_login`, …

## NZBN API

Set `BUSINESS_GOVT_API_KEY` (or `NZBN_API_KEY`) for live read-only calls to the business.govt.nz gateway. Without a key, `nzbn_lookup` returns offline human-action guidance and **does not invent NZBNs**.

## Security notes

- Company memory is local by default (`memory/companies/`).
- Runtime company data is gitignored.
- Never store IRD numbers, bank credentials, or API keys in memory files.
