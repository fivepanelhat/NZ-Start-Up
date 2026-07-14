# Company Memory Schema

Root: `memory/companies/<company-id>/`

```text
profile.md              # Non-secret company facts
decisions.md            # Append-only decision log
calendar.md             # Compliance and filing deadlines
pipeline.md             # GTM stages
runway.md               # Finance snapshot (no bank passwords)
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
