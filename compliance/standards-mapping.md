# Standards mapping — procurement & due-diligence collateral

**Product:** NZ Start-Up in a Box · Coastal Alpine Tech Limited (Pre-seed)  
verified: 2026-07-15  
**Version:** 1.6.1  

Maps existing engineering controls to frameworks EDAs, councils, and investors ask about.
This is **alignment evidence**, not a certification claim.

---

## OWASP LLM Top 10 (2025)

| Control | Implementation | Evidence |
|---------|----------------|----------|
| LLM01 Prompt injection | Inbound quarantine with **nonce delimiters** + injection flags; policy treats external text as data | `nz_startup/untrusted.py`, bank/invoice wiring, `tests/fixtures/injection_corpus.txt`, `tests/test_v15_gap.py` |
| LLM02 Insecure output handling | Watermarks; no send/file/pay tools on MCP surface | `hitl.py`, `mcp_server.py`, `agent_guardrails.py` |
| LLM03 Training data poisoning | N/A (no training pipeline); knowledge is dated + re-verified | `knowledge/*.md` `verified:`, `scripts/check_knowledge_freshness.py` |
| LLM04 Model DoS | Per-company token budget + optional hard cap | `model_routing.py`, `nz-startup budget` |
| LLM05 Supply chain | Lockfile + pip-audit CI; pack SHA256 + SBOM | `requirements-lock.txt`, `.github/workflows/skills-ci.yml`, `nz-startup pack` |
| LLM06 Sensitive info disclosure | Secret-pattern refusal on memory write; no secrets in git | `agent_guardrails.py`, `SECURITY.md`, `.gitignore` |
| LLM07 Insecure plugin design | Forbidden tool names; default-deny action allow-list | `hitl.py` FORBIDDEN_TOOL_NAMES + ALLOWED_AUTONOMY_VERBS |
| LLM08 Excessive agency | Autonomy ceiling: inform/draft/prepare/monitor/remind only | `COMPLIANCE.md`, `compliance/hitl-matrix.md` |
| LLM09 Overreliance | Honest degradation (NZBN offline); drafts watermarked | `nzbn.py`, WATERMARKS |
| LLM10 Model theft | Proprietary dual licence; no model weights shipped | `LICENSE`, `docs/DUAL_LICENCE.md` |

---

## NIST AI RMF (Govern / Map / Measure / Manage)

| Function | Our practice | Evidence |
|----------|--------------|----------|
| **Govern** | HITL matrix, dual licence, cultural non-extraction | `compliance/hitl-matrix.md`, `AGENTS.md`, Te Mana Raraunga docs |
| **Map** | Risk tiers on skills/actions; model_tier by stakes | `agent_guardrails.classify_risk`, skill `model_tier` frontmatter |
| **Measure** | Golden evals (deterministic CI + opt-in live), audit telemetry | `nz_startup/evals.py`, `audit.jsonl`, `nz-startup eval` |
| **Manage** | Compliance gate, doctor, smoke, schedule cadence, backups | `compliance_gate.py`, `doctor.py`, `schedule.py`, `backup.py` |

---

## ISO/IEC 42001 (AI management systems) — control themes

| Theme | Implementation | Evidence |
|-------|----------------|----------|
| AI policy | Autonomy slogan + pure policy banner | `agent_guardrails.HARNESS_BANNER`, COMPLIANCE.md |
| Risk assessment | RiskTier + HITL required flags | `classify_risk`, audit `risk_level` |
| Data quality / provenance | Knowledge freshness; pack SHA256/SBOM | G4 CI, T4 packaging |
| Human oversight | Default-deny allow-list; console session token | `hitl.py`, `console.py` |
| Lifecycle | Versioned releases, CHANGELOG, eval reports | `CHANGELOG.md`, `evals/` |
| Transparency | Files-as-memory; board pack fleet cost | `memory/companies/*`, board pack |

---

## NZ Algorithm Charter (public-sector buyers)

| Charter principle | Product alignment | Evidence |
|-------------------|-------------------|----------|
| Transparency | Local files, greppable audit, no black-box decisions on filings | `audit.jsonl`, company memory markdown |
| Partnership | HITL — humans advise/sign/file/send/pay | Autonomy slogan everywhere |
| People | Cultural sensitivity flags; Te Mana Raraunga | skill `cultural_sensitivity`, compliance docs |
| Data | Local-first; encrypted backups; no multi-tenant SaaS default | `backup.py`, CONSOLE localhost bind |
| Privacy | Privacy Act 2020 notes; PII patterns blocked from git paths | `compliance/privacy-act-2020.md` |
| Human rights | No automated government session use (RealMe/myIR) | G15 watch-only boundary |

---

## Privacy Act 2020 (NZ) — IPP alignment (summary)

| IPP theme | Alignment | Evidence |
|-----------|-----------|----------|
| Purpose / collection | Founder-owned local memory; purpose = operating assist | memory schema, onboard flow |
| Storage / security | Localhost console token; encrypted backup; disk encryption assumed | G11, T7, SECURITY.md |
| Access / correction | Founder has filesystem access to all company data | `memory/companies/<id>/` |
| Disclosure | Agents do not email or upload customer data | FORBIDDEN tools, no webhooks |
| Cross-border | Default local-first; sovereign inference preferred | SECURITY.md, AGENTS.md |

---

## How to use this document

1. Attach to EDA / council RFIs as **control mapping** (not a certificate).  
2. Point assessors at `nz-startup compliance check` + test suite.  
3. Re-verify after material architecture changes; bump **Verified** date above.

**Not legal advice.** Independent NZ legal review for regulated deployments.
