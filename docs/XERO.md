# Xero read-only adapter (v0.4)

## Purpose

Give the **Finance Clerk** a local, audited view of Xero data without granting agents payment or filing powers.

## HITL

| Allowed | Forbidden |
|---------|-----------|
| Read organisation | Create/update invoices |
| Read authorised invoices (page) | Create payments |
| Read accounts list (names) | Bank transfers |
| Write snapshot under `finance/` | Store tokens in memory/git |

## Setup

1. Create a Xero app with **read** scopes only (e.g. `accounting.transactions.read`, `accounting.settings.read`).
2. Complete OAuth; obtain access token + tenant id.
3. Set environment (never commit):

```bash
export XERO_ACCESS_TOKEN="..."
export XERO_TENANT_ID="..."
# optional refresh
export XERO_CLIENT_ID="..."
export XERO_CLIENT_SECRET="..."
export XERO_REFRESH_TOKEN="..."
```

4. Snapshot:

```bash
nz-startup xero status
nz-startup xero snapshot my-startup
# or force offline demo:
nz-startup xero snapshot my-startup --offline
```

## Outputs

- `memory/companies/<id>/finance/xero-snapshot.json`
- `memory/companies/<id>/finance/xero-snapshot.md`
- Note appended to `runway.md`

## Offline mode

Without credentials, snapshot is a **demo/guidance** payload so skills still run in dogfood. No invented bank balances.
