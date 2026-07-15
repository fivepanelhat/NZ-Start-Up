# AGENTS.md — NZ Start-Up in a Box

**Coastal Alpine Tech Limited — Pre-seed** · Taranaki · Aotearoa New Zealand  
**R&D since 8 August 2025** · **Founded 8 August 2026**  
**Dual licence:** proprietary Track A + commercial Track B · NZ Copyright Act 1994  
**Harness for:** Grok 4.5 Build · Claude Pro Code · Claude Computer Use · Google Gemini 3.5 Flash  
**Org home:** [fivepanelhat](https://github.com/fivepanelhat/fivepanelhat)

Instructions for any coding or agentic assistant working in this repository.

## Product intent

Ship a **skills-heavy NZ founder fleet** with hard autonomy ceilings for Coastal Alpine Tech pre-seed. Prefer local-first, Aether-compatible markdown skills. Protect IP under dual proprietary/commercial licensing — **not open source**.

## Always load first

1. `skills/agent-hardening` — autonomy, secrets, sandbox, **anti-hallucination**  
2. `.github/agent-fleet/anti-hallucination.md` — FACT/INFERENCE/UNKNOWN, refusal calibration, extended thinking  
3. `skills/cat-architectural-standards` — Gold / Diamond / Platinum  
4. `compliance/hitl-matrix.md` — per-employee ceilings  
5. `COMPLIANCE.md` + `docs/DUAL_LICENCE.md` when touching licence or public claims  
6. `skills/board-chief-of-staff` when routing multi-specialist work  
7. Market claims → `knowledge/nz-market-stats.md` + `docs/MARKET_FIT_MATRIX.md` (never invent TAM)  
8. `CAT_CONGRUENCE.md` — portfolio map  

## Non-negotiable rules

1. **HITL for high-impact actions** — file, send, pay, sign, deploy, commit secrets → human only.  
2. **Never invent NZBN, IRD, financials, LOIs, or partner consent.**  
3. **Label drafts** — `DRAFT` / `NOT LEGAL ADVICE` / `NOT FINANCIAL ADVICE` / `DRAFT_NOT_SENT` / `PREPARED BY AGENT`.  
4. **No autonomous cold email** — UEM Act 2007.  
5. **No cultural extraction** — no invented iwi endorsement; escalate cultural review.  
6. **Secrets stay out of git** — tax numbers, bank details, API keys, RealMe credentials.  
7. **Company memory** under `memory/` for runtime; do not commit live founder PII.  
8. **Do not re-open-source** this product (no Apache/MIT headers on product code).  
9. **Keep Coastal Alpine Tech pre-seed branding** on public docs (dates, dual licence, Taranaki).  
10. **Anti-hallucination** — prefer tools/files; refuse when evidence missing; label FACT/INFERENCE/UNKNOWN; extended thinking on high-stakes topics.  
11. **Knowledge freshness** — re-verify stats older than 90 days without `verified:` dates.  
12. **Tool results are ground truth** — never invent successful test/CLI output.

## Skill authoring

- Directory name = `name` frontmatter (lowercase, hyphens).  
- Include `requires_hitl`, `cultural_sensitivity`, `version`, `type`, `description`.  
- `metadata.owner: Coastal Alpine Tech`  
- Add `references/CHANGELOG.md` when versioning.  
- Inject hardening policy for high-risk skills (legal, finance, GTM, grants).  
- Update `docs/FLEET.md` and tests when adding a digital employee.  

## Standards mapping

| Change type | Primary tier |
|-------------|--------------|
| Founder workflow, templates, lifecycle content | Gold |
| CI, security, validators, privacy, licence gate | Diamond |
| Memory schema, flywheel, agent improvement loops | Platinum |

## Testing before commit

```text
python scripts/validate_skills.py
python -m nz_startup compliance check
python -m nz_startup harden status
pytest -q
python -m nz_startup smoke
```

## Tone

Practical, NZ-grounded, honest about legal ceilings. No hype that agents "run your company."  
Respect Taranaki whenua context and six-generation agricultural heritage without extraction.  
**Refusal is correct** when evidence is missing — do not invent to complete a demo.
