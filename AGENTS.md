# AGENTS.md — NZ Start-Up in a Box

**Coastal Alpine Tech Limited — Pre-seed** · Taranaki · Aotearoa New Zealand  
**R&D since 8 August 2025** · **Founded 8 August 2026**  
**Dual licence:** proprietary Track A + commercial Track B · NZ Copyright Act 1994  
**Harness for:** Grok 4.5 Build · Claude Pro Code · Claude Computer Use · Google Gemini 3.5 Flash

Instructions for any coding or agentic assistant working in this repository.

## Product intent

Ship a **skills-heavy NZ founder fleet** with hard autonomy ceilings for Coastal Alpine Tech pre-seed. Prefer local-first, Aether-compatible markdown skills. Protect IP under dual proprietary/commercial licensing — **not open source**.

## Always load first

1. `skills/agent-hardening` — autonomy ceilings, secrets, sandbox  
2. `skills/cat-architectural-standards` — Gold / Diamond / Platinum  
3. `compliance/hitl-matrix.md` — per-employee ceilings  
4. `COMPLIANCE.md` + `docs/DUAL_LICENCE.md` when touching licence or public claims  
5. `skills/board-chief-of-staff` when routing multi-specialist work  

## Non-negotiable rules

1. **HITL for high-impact actions** — file, send, pay, sign, deploy, commit secrets → human only.  
2. **Never invent NZBN, IRD, financials, or partner consent.**  
3. **Label drafts** — `DRAFT — NOT FOR SUBMISSION` / `NOT LEGAL ADVICE` / `NOT FINANCIAL ADVICE` / `DRAFT_NOT_SENT`.  
4. **No autonomous cold email** — UEM Act 2007.  
5. **No cultural extraction** — do not invent iwi endorsement; Wayne Roberts / Taranaki whānau agricultural heritage is founding context, not a free marketing skin. Escalate cultural review.  
6. **Secrets stay out of git** — tax numbers, bank details, API keys, RealMe credentials.  
7. **Company memory** under `memory/` for runtime; do not commit live founder PII.  
8. **Do not re-open-source** this product (no Apache/MIT headers on product code).  
9. **Keep Coastal Alpine Tech pre-seed branding** on public docs (dates, dual licence, Taranaki).  

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

Practical, NZ-grounded, honest about legal ceilings. No hype that agents “run your company.”  
Respect Taranaki whenua context and six-generation agricultural heritage without extraction.
