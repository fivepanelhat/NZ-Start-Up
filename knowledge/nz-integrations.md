---
verified: 2026-07-15
status: active
max_age_days: 90
---

# NZ Integrations Map

Living list - verify URLs and API terms before production use.

| System | Use in fleet | Access pattern | Notes |
|--------|--------------|----------------|-------|
| Companies Office / NZBN | Formation, compliance, firmographics | api.business.govt.nz (when credentialed) | Founder files; agent prepares |
| IRD | GST/income tax prep | Human myIR | No agent filing |
| RDTI | Eligibility + claims support | rdti.govt.nz | Contemporaneous logs critical |
| MBIE / post-Callaghan landscape | Grants | Web + EDA | Landscape moves - re-verify |
| Regional EDAs (e.g. Venture Taranaki) | ScaleUp, PowerUp, intros | Human relationship | Primary B2B buyer channel for white-label |
| Employment NZ / MBIE employment | First hire checklists | Public guidance | Not employment law advice |
| WorkSafe | H&S basics | Public guidance | Not full risk assessment |
| Stats NZ | Market sizing | Public data | Cite sources |
| GETS / tenders | Optional procurement navigator | Public | Later skill |
| Xero / QuickBooks | Finance clerk | OAuth read-only preferred | Never store full credentials in git |
| HubSpot / CRM | GTM | MCP drafts-only | Send = HITL |
| RealMe | Filing identity | Human only | Never automate credentials |

## Integration principle

Prefer **read + draft** over **write + submit**. Every write to government or customer channel is a HITL gate.
