# Golden behavioural evals (G1)

Deterministic golden scenarios for fleet skills. Run:

```bash
nz-startup eval --write
# or
python -m nz_startup eval --json
```

CI runs the suite on every push. Cases live in `nz_startup/evals.py`.

| ID | Skill | Intent |
|----|-------|--------|
| hitl_allowlist_default_deny | agent-hardening | Novel high-risk phrasing blocked |
| ingest_quarantine_injection | agent-hardening | Inbound injection flagged |
| grants_rdti_log_week | grants-rdti-clerk | Contemporaneous RDTI log |
| finance_bank_import_triage | finance-clerk | Bank CSV triage |
| gtm_pipeline_add | gtm-pipeline-rep | Pipeline deal append |

LLM-as-judge can be layered later; v1.5 keeps CI free of live model calls.
