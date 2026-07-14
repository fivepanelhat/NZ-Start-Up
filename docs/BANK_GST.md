# Bank feed + GST assist (v0.5)

## Bank feed

Human exports CSV from their bank → agent imports and triages.

```bash
nz-startup bank import my-startup --file ./exports/transactions.csv
nz-startup bank triage my-startup
nz-startup bank list my-startup --direction outflow --limit 20
```

### Expected columns

Flexible headers. Preferred:

| Column | Aliases |
|--------|---------|
| Date | Transaction Date, Posted, Value Date |
| Description | Narrative, Details, Memo, Payee |
| Amount | Value, NZD — **or** Debit + Credit |
| Balance | optional |

Sample: `templates/bank-feed-sample.csv`

### Outputs

- `finance/bank-feed.csv` (source of truth)
- `finance/bank-feed.md`
- `finance/bank-imports/` archived originals

## GST working papers

```bash
# Optional: refresh Xero read-only snapshot first
nz-startup xero snapshot my-startup --offline

nz-startup gst prepare my-startup --start 2026-07-01 --end 2026-07-31
```

### Outputs

- `finance/gst/gst-worksheet-<start>_to_<end>.md`
- matching `.json` and `-lines.csv`
- `finance/gst/gst-worksheet-latest.md`

### Hard boundaries

| Agent may | Agent must not |
|-----------|----------------|
| Import bank CSV | Connect to bank APIs / move money |
| Guess categories | Certify GST treatment |
| Estimate GST from inclusive bank totals | File myIR / pay IRD |
| Combine Xero snapshot context | Create Xero payments |

**NOT A TAX FILING.** Confirm with an accountant.
