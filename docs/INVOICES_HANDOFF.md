# Invoice triage + accountant handoff (v0.6)

## Invoice triage

```bash
# Single file (txt/md/pdf)
nz-startup invoice triage my-startup --path ./inbox/invoice.pdf

# Whole folder
nz-startup invoice triage my-startup --path ./inbox/

nz-startup invoice list my-startup
```

### Extraction

| Input | Method |
|-------|--------|
| `.txt` / `.md` | Direct read |
| `.pdf` | `pypdf` if installed (`pip install '.[pdf]'`), else noisy raw string fallback |
| images | Flagged for human OCR (no cloud OCR bundled) |

### Outputs

- `finance/invoices/inbox/` - archived originals 
- `finance/invoices/triaged/<id>/` - `triage.md`, `triage.json`, `extracted.txt` 
- `finance/invoices/invoice-registry.csv` + `.md` 

**Human must verify** tax invoice validity before any GST claim.

## Accountant handoff pack

```bash
nz-startup handoff pack my-startup --label accountant
```

Creates:

- `handoff/handoff-accountant-YYYY-MM-DD.zip`
- `handoff/handoff-latest.zip`
- `handoff/HANDOFF_README.md`

Includes (when present): bank feed, GST papers, invoice registry, Xero snapshot, runway, RDTI log, calendar, latest weekly board, deadline digest.

### HITL

| Agent may | Agent must not |
|-----------|----------------|
| Extract invoice fields locally | Certify tax invoices |
| Zip working papers | Email/upload the zip |
| Flag low confidence | Claim GST or file myIR |
