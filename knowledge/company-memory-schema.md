---
verified: 2026-07-15
status: active
max_age_days: 90
---

# Company Memory Schema

Root: `memory/companies/<company-id>/`

```text
profile.md              # Non-secret company facts
decisions.md            # Append-only decision log
calendar.md             # Synced view of calendar.csv
calendar.csv            # Compliance deadlines (source of truth)
pipeline.md             # Synced view of pipeline.csv
pipeline.csv            # CRM-lite deals (source of truth)
grants-tracker.md       # Synced view of grants-tracker.csv
grants-tracker.csv      # Funding opportunities (source of truth)
runway.md               # Finance snapshot (no bank passwords)
finance/
  xero-snapshot.json    # Xero read-only snapshot (no tokens)
  xero-snapshot.md
  bank-feed.csv         # Imported bank transactions (normalized)
  bank-feed.md
  bank-imports/         # Archived raw bank CSVs
  gst/                  # GST working papers (not filings)
  invoices/
    inbox/              # Archived invoice originals
    triaged/            # Per-invoice extraction
    invoice-registry.csv
handoff/                # Accountant zip packs
exports/
  deadlines-latest.ics  # Importable calendar
  deadline-digest-latest.md
rdti-log.csv            # R&D activity log
audit.jsonl             # Agent audit trail
weekly/                 # Board reports
drafts/
  outreach/
  legal/
  grants/
  content/
incorporation-pack/
checklists/
```

## profile.md minimum fields

- Legal name (or proposed)  
- Trading name  
- Entity type (Ltd, etc.)  
- Region  
- NZBN (when issued)  
- Directors (names only)  
- Wedge / ICP one-liner  
- Cultural partnerships (if any — factual only)  
- Data residency preference (local default)

## Write rules

1. Never store IRD numbers, bank account numbers, or API keys in memory files committed to git.  
2. Material decisions get a dated line in `decisions.md`.  
3. Specialists update only their owned fields unless Board skill consolidates.  
