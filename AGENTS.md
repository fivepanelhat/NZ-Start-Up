# AGENTS.md — NZ Start-Up in a Box

Instructions for any coding or agentic assistant working in this repository.

## Product intent

Ship a **skills-heavy NZ founder fleet** with hard autonomy ceilings. Prefer local-first, Aether-compatible markdown skills over multi-tenant SaaS complexity.

## Always load first

1. `skills/cat-architectural-standards` — classify work Gold / Diamond / Platinum
2. `compliance/hitl-matrix.md` — check autonomy ceiling
3. `skills/board-chief-of-staff` when routing multi-specialist work

## Non-negotiable rules

1. **HITL for high-impact actions** — file, send, pay, sign, deploy, commit secrets → human only.
2. **Never invent NZBN, IRD, financials, or partner consent.**
3. **Label drafts** — `DRAFT — NOT FOR SUBMISSION` / `NOT LEGAL ADVICE` / `NOT FINANCIAL ADVICE`.
4. **No autonomous cold email** — UEM Act 2007.
5. **No cultural extraction** — do not add Māori framing without real partnership path; escalate cultural review.
6. **Secrets stay out of git** — tax numbers, bank details, API keys, RealMe credentials.
7. **Company memory** under `memory/` for runtime; do not commit live founder PII.

## Skill authoring

- Directory name = `name` frontmatter (lowercase, hyphens).
- Include `requires_hitl`, `cultural_sensitivity`, `version`, `type`, `description`.
- Put custom fields under `metadata:` when using strict Claude skill validators.
- Add `references/CHANGELOG.md` when versioning.
- Update `docs/FLEET.md` and tests when adding a digital employee.

## Standards mapping

| Change type | Primary tier |
|-------------|--------------|
| Founder workflow, templates, lifecycle content | Gold |
| CI, security, validators, privacy defaults | Diamond |
| Memory schema, flywheel, agent improvement loops | Platinum |

## Testing before commit

```text
python scripts/validate_skills.py
pytest -q
```

## Tone

Practical, NZ-grounded, honest about legal ceilings. No hype that agents “run your company.”
