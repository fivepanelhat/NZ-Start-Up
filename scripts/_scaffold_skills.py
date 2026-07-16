"""One-shot scaffold for fleet skills, templates, and example memory. Run from repo root."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8", newline="\n")
    print("wrote", rel)


SKILLS = {
    "cat-architectural-standards": {
        "version": "1.0.0",
        "type": "orchestration",
        "requires_hitl": True,
        "cultural_sensitivity": "high",
        "description": (
            "Classify and govern NZ Start-Up in a Box work under CAT Gold, Diamond, "
            "and Platinum standards. Use for planning, reviews, HITL gates, and maturity checks."
        ),
        "tags": ["cat", "gold", "diamond", "platinum", "governance"],
        "title": "CAT Architectural Standards",
        "body": """
## Overview
Top-level governance skill for Coastal Alpine Tech and NZ Start-Up in a Box.
Operationalises Gold (workflow), Diamond (foundation), and Platinum (intelligence flywheel).

## When to Use
- Starting any non-trivial planning or architecture session
- Reviewing whether work claims a maturity tier honestly
- Before release or white-label packaging

## Instructions

### 1. Classify
State primary and secondary tier:
- **Gold** — founder lifecycle / process mapping / templates
- **Diamond** — CI, security, privacy, production hygiene
- **Platinum** — memory, agents, flywheel, learning loops

### 2. Apply tier rules
- Gold → linear phase gates; map to real NZ founder steps
- Diamond → security, validation, audit, no secrets
- Platinum → capture points, company memory writes, evaluation

### 3. HITL
Load `compliance/hitl-matrix.md`. Block forbidden autonomies.

### 4. Cultural overlay
Load `compliance/te-mana-raraunga.md` for all tiers.

## Guardrails
- Never claim Diamond without CI/security evidence
- Never treat Platinum as "add more AI" without Gold workflow
- HITL for cultural, health, funding pathway claims

## Output
```markdown
## Classification
- Primary: Gold|Diamond|Platinum
- Secondary: ...
- HITL required: yes/no
- Cultural review: yes/no
- Proceed: ...
```

## References
- `docs/STANDARDS.md`
- `standards/*.md`
- `references/CHANGELOG.md`
""",
    },
    "formation-officer": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "medium",
        "description": (
            "Prepare NZ company formation packs including name checks, constitution options, "
            "share structure notes, IRD GST prep, and NZBN steps. Founder files via RealMe."
        ),
        "tags": ["formation", "companies-office", "nzbn", "ird"],
        "title": "Formation Officer",
        "body": """
## Overview
Digital employee #1. Builds incorporation readiness packs for NZ limited companies.
**Does not file.** Founder authenticates with RealMe (or uses an authorised agent).

## When to Use
- Pre-incorporation checklists
- Name availability research notes
- Constitution / share structure option papers
- IRD number and GST registration prep lists

## Instructions
1. Read company memory `profile.md` (create if missing).
2. Produce incorporation pack under `incorporation-pack/`:
   - `name-options.md`
   - `structure-options.md`
   - `checklist.md`
   - `ird-gst-prep.md`
3. Use `templates/incorporation-checklist.md`.
4. Link NZ systems from `knowledge/nz-integrations.md`.
5. End with **Human action checklist** (file, pay, bank).

## Guardrails
- Never claim name is "available" without noting verification is on Companies Office
- Never complete RealMe or pay reservation fees
- Information only — not legal advice on constitution

## Output header
```markdown
# DRAFT — NOT FOR SUBMISSION
Skill: formation-officer
HITL: founder must file in own authenticated session
```

## References
- `templates/incorporation-checklist.md`
- `knowledge/nz-integrations.md`
""",
    },
    "compliance-registrar": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "medium",
        "description": (
            "Maintain NZ compliance calendars and checklists for annual returns, Privacy Act, "
            "H and S basics, and first-hire employment law prompts. Never self-certifies."
        ),
        "tags": ["compliance", "privacy", "companies-act", "employment"],
        "title": "Compliance Registrar",
        "body": """
## Overview
Digital employee #2. Deadline intelligence and records-keeping prompts under NZ regimes.
**Never certifies** that the company is compliant.

## When to Use
- Annual return reminders
- Privacy Act obligations checklist
- H&S basics before farm/worksite pilots
- First hire employment checklist

## Instructions
1. Update `calendar.md` with dated obligations.
2. Draft checklists into `checklists/` using templates.
3. Label all outputs: `INFORMATION ONLY — not a compliance certificate`.
4. Escalate legal questions to human + lawyer.

## Guardrails
- Lawyers and Conveyancers Act boundary
- WorkSafe guidance is not a full risk assessment
- Employment NZ content is checklist-level only

## References
- `templates/annual-return-checklist.md`
- `compliance/privacy-act-2020.md`
- `compliance/legal-boundaries-nz.md`
""",
    },
    "grants-rdti-clerk": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "high",
        "description": (
            "Grant radar, eligibility screening, application drafting, and contemporaneous RDTI "
            "R and D activity logging from commits or timesheets. Human submits applications."
        ),
        "tags": ["grants", "rdti", "funding", "eda"],
        "title": "Grants and RDTI Clerk",
        "body": """
## Overview
Digital employee #3. High autonomy on **logging and monitoring**; human submits applications.
RDTI contemporaneous logging is a core product habit — retroactive fiction fails claims.

## When to Use
- Discover open grants / EDA programmes
- Fit-score a project
- Draft EOI or application sections
- Append RDTI activity log from provided evidence

## Modes
### Discover
Rank opportunities from `knowledge/funding-landscape.md` + live verification when possible.

### Fit-score
Score 0–100 with go/no-go reasons; flag co-fund conflicts.

### Draft
Write `DRAFT — NOT FOR SUBMISSION` application sections; mark VERIFIED vs NEEDS_EVIDENCE.

### Log RDTI
Append rows to `rdti-log.csv` only from user-provided commits/hours/uncertainty notes.
Never invent hours.

## Guardrails
- No false RDTI claims
- Cultural review for Māori funds without relationship pathway
- Secrets (bank details) never in drafts committed to git

## References
- `templates/rdti-activity-log.csv`
- `templates/grant-application-draft.md`
- `knowledge/funding-landscape.md`
- Aether `grants-agent` patterns
""",
    },
    "market-validator": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": False,
        "cultural_sensitivity": "low",
        "description": (
            "Market sizing, competitor briefs, pricing research, and interview-guide generation "
            "with sources and confidence labels for NZ startups."
        ),
        "tags": ["market", "validation", "research"],
        "title": "Market Validator",
        "body": """
## Overview
Digital employee #4. Research-heavy, fully autonomous for research synthesis.
Conclusions must carry **confidence + sources**.

## When to Use
- TAM/SAM/SOM style sizing (honest NZ numbers)
- Competitor briefs
- Pricing comps
- Customer interview guides

## Instructions
1. Prefer Stats NZ and citable public sources.
2. Separate facts / inferences / unknowns.
3. Write report to `drafts/` or memory using `templates/market-validation-report.md`.
4. Never fabricate statistics.

## Output
Include confidence (high/medium/low) per major claim.
""",
    },
    "gtm-pipeline-rep": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "low",
        "description": (
            "Build ICP lists, personalised outreach drafts, CRM hygiene notes, meeting prep, "
            "and proposals. Sends nothing without human approval under UEM Act constraints."
        ),
        "tags": ["gtm", "pipeline", "sales", "uem"],
        "title": "GTM Pipeline Rep",
        "body": """
## Overview
Digital employee #5. Drafts everything; **sends nothing** without approval.
NZ Unsolicited Electronic Messages Act 2007 makes autonomous cold email a legal risk.

## When to Use
- ICP list construction
- Outreach email drafts
- Meeting prep / follow-ups
- Pilot proposal generation from templates

## Instructions
1. Update `pipeline.md` stages.
2. Write drafts under `drafts/outreach/` with status `DRAFT_NOT_SENT`.
3. Provide human send checklist (consent, unsubscribe, accurate identity).
4. Never call send APIs.

## Guardrails
- UEM Act 2007
- No invented personal emails or phone numbers
- No fake social proof

## References
- `templates/outreach-draft.md`
- `compliance/hitl-matrix.md`
""",
    },
    "content-comms-officer": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "medium",
        "description": (
            "One-asset five-outputs content engine for LinkedIn, build-logs, press kit upkeep, "
            "media pitches, and event calendars. Schedules only pre-approved content."
        ),
        "tags": ["content", "comms", "linkedin", "media"],
        "title": "Content and Comms Officer",
        "body": """
## Overview
Digital employee #6. Multiplies one founder asset into channel-ready drafts.
Voice profile should be trained per founder when available.

## When to Use
- LinkedIn posts from build footage notes
- Build-log drafts
- Press kit maintenance
- Media pitch drafts

## One-asset-five-outputs
From a single source (demo note, pilot story, release):
1. LinkedIn post
2. Short build-log
3. Email newsletter blurb
4. Media pitch angle
5. Event talk abstract

## Guardrails
- Schedule/publish only if human marked pre-approved
- No cultural extraction or false iwi claims
- No medical or over-claiming AI performance claims
""",
    },
    "finance-clerk": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "low",
        "description": (
            "Bookkeeping triage, invoice chase drafts, GST return prep worksheets, cash-flow "
            "forecasts, and runway alerts. Never moves money or acts as a tax agent."
        ),
        "tags": ["finance", "gst", "runway", "xero"],
        "title": "Finance Clerk",
        "body": """
## Overview
Digital employee #7. Prepares finance artefacts from provided figures.
Human or accountant files. **Never moves money.**

## When to Use
- Categorisation triage suggestions
- Invoice chase email drafts (still HITL to send)
- GST worksheet prep
- Burn / runway alerts

## Instructions
1. Update `runway.md` from user-supplied numbers only.
2. Use `templates/gst-prep-checklist.md`.
3. Flag tax-agent boundary on every filing-related artefact.

## Guardrails
- No inventing bank balances
- No storing account credentials
- Not a substitute for a chartered accountant
""",
    },
    "funding-analyst": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "medium",
        "description": (
            "Investor targeting, data-room assembly, deck iteration support, cap-table scenarios, "
            "and SAFE term comparison. Flags lawyer review under FMCA boundaries."
        ),
        "tags": ["funding", "investors", "safe", "cap-table"],
        "title": "Funding Analyst",
        "body": """
## Overview
Digital employee #8. Full autonomy on **prep**; term recommendations always flagged for lawyer.

## When to Use
- Thesis-matched NZ investor lists
- Data room index
- Deck outline iteration
- Cap table scenarios / SAFE comparison education

## Guardrails
- NOT FINANCIAL ADVICE
- FMCA may apply — lawyer review required before relying on term recommendations
- No fabricated traction metrics

## References
- `templates/investor-data-room-index.md`
""",
    },
    "legal-document-assistant": {
        "version": "0.1.0",
        "type": "workflow",
        "requires_hitl": True,
        "cultural_sensitivity": "medium",
        "description": (
            "First drafts of pilot agreements, NDAs, terms, privacy policies, and employment "
            "offers from NZ-oriented outlines. Watermarked not legal advice."
        ),
        "tags": ["legal", "nda", "privacy", "contracts"],
        "title": "Legal Document Assistant",
        "body": """
## Overview
Digital employee #9. Drafts only. Unauthorised legal practice is an offence —
this skill must never present as a lawyer.

## When to Use
- NDA / pilot / ToS / privacy outline drafts
- Employment offer outlines (first hire)
- Privacy Act checklist crosswalk

## Instructions
1. Start from `templates/*-outline.md`.
2. Customise with company memory facts (non-secret).
3. Header every doc with watermark.
4. List open issues for lawyer.

## Watermark
```text
DRAFT — NOT LEGAL ADVICE — independent NZ legal review required before use
```

## References
- `templates/nda-outline.md`
- `templates/pilot-agreement-outline.md`
- `templates/privacy-policy-outline.md`
- `templates/employment-offer-outline.md`
""",
    },
    "board-chief-of-staff": {
        "version": "0.1.0",
        "type": "orchestration",
        "requires_hitl": True,
        "cultural_sensitivity": "high",
        "description": (
            "Orchestrator for the NZ Start-Up fleet. Runs weekly operating reviews, routes founder "
            "requests to specialists, maintains company memory, and escalates without deciding."
        ),
        "tags": ["orchestrator", "board", "weekly-review", "fleet"],
        "title": "Board Chief of Staff",
        "body": """
## Overview
Digital employee #10 — the interface. Aggregates pipeline vs plan, cash vs runway,
compliance deadlines, and top-3 priorities. **Escalates, never decides.**

## When to Use
- Weekly operating review
- Routing a founder request to the right specialist skill
- Consolidating company memory
- Preparing EDA / mentor meeting packs

## Weekly review algorithm
1. Load `cat-architectural-standards` classification for the week.
2. Read memory: profile, pipeline, runway, calendar, rdti-log, recent drafts.
3. Produce `weekly/YYYY-MM-DD.md` from `templates/weekly-operating-review.md`.
4. Propose next specialist tasks (do not auto-execute forbidden actions).
5. Append decision prompts for the human.

## Routing table
| Founder ask contains | Route to |
|----------------------|----------|
| incorporate, NZBN, constitution | formation-officer |
| annual return, privacy, H&S, hire | compliance-registrar |
| grant, RDTI, EDA | grants-rdti-clerk |
| market size, competitor | market-validator |
| outreach, pipeline, ICP | gtm-pipeline-rep |
| LinkedIn, press, content | content-comms-officer |
| GST, runway, invoice | finance-clerk |
| investor, SAFE, deck | funding-analyst |
| NDA, pilot contract, ToS | legal-document-assistant |

## Guardrails
- Never impersonate board approval
- Never file, send, or pay
- Cultural review flags bubble up

## References
- `docs/FLEET.md`
- `templates/weekly-operating-review.md`
- `knowledge/company-memory-schema.md`
""",
    },
    "nz-startup-fleet": {
        "version": "0.1.0",
        "type": "orchestration",
        "requires_hitl": True,
        "cultural_sensitivity": "high",
        "description": (
            "Product entry skill for NZ Start-Up in a Box. Bootstraps company memory, explains "
            "the fleet, and starts dogfooding with CAT standards and HITL compliance."
        ),
        "tags": ["fleet", "bootstrap", "product", "nz-startup"],
        "title": "NZ Start-Up Fleet",
        "body": """
## Overview
Meta skill for the product. Use when the user installs the pack or says
"run my NZ startup agents" / "startup in a box".

## Bootstrap sequence
1. Load `cat-architectural-standards` — classify session (usually Gold + Platinum).
2. Ensure company memory exists (copy example structure).
3. Introduce the 10 digital employees and autonomy slogan.
4. Offer one of: formation pack | weekly board | RDTI log start | GTM draft week.
5. Remind hard boundaries (file/send/pay = human).

## Dogfood mode (Coastal Alpine Tech)
- Map 30/60/90 plan actions to fleet skills
- Prefer paid pilot pipeline discipline over new product forks
- Weekly board report is the demo for EDA white-label conversations

## Guardrails
- Do not promise autonomous company operation
- Do not skip compliance docs on first run

## References
- `README.md`
- `docs/GETTING_STARTED.md`
- `docs/FLEET.md`
""",
    },
}


def skill_md(name: str, meta: dict) -> str:
    tags = ", ".join(meta["tags"])
    fm = f"""---
name: {name}
version: "{meta['version']}"
type: {meta['type']}
requires_hitl: {str(meta['requires_hitl']).lower()}
cultural_sensitivity: {meta['cultural_sensitivity']}
description: >
  {meta['description']}
metadata:
  status: active
  owner: Coastal Alpine Tech
  product: nz-startup-in-a-box
  standards: [gold, diamond, platinum]
  last_updated: "2026-07-14"
tags:
{chr(10).join('  - ' + t for t in meta['tags'])}
---

# {meta['title']}
{meta['body']}
"""
    return fm


def main() -> None:
    for name, meta in SKILLS.items():
        w(f"skills/{name}/SKILL.md", skill_md(name, meta))
        w(
            f"skills/{name}/references/CHANGELOG.md",
            f"""# Changelog — {name}

## {meta['version']} — 2026-07-14
- Initial release for NZ Start-Up in a Box v0.1.0
""",
        )

    # Shared references for CAT
    w(
        "skills/cat-architectural-standards/references/Skills_to_Tiers_Mapping.md",
        """# Skills to Tiers Mapping — NZ Start-Up Fleet

| Skill | Primary | Secondary |
|-------|---------|-----------|
| cat-architectural-standards | All | — |
| nz-startup-fleet | Platinum | Gold |
| board-chief-of-staff | Platinum | Gold |
| formation-officer | Gold | Diamond |
| compliance-registrar | Gold | Diamond |
| grants-rdti-clerk | Gold | Platinum |
| market-validator | Gold | Platinum |
| gtm-pipeline-rep | Gold | — |
| content-comms-officer | Gold | — |
| finance-clerk | Gold | Diamond |
| funding-analyst | Gold | — |
| legal-document-assistant | Gold | Diamond |
""",
    )

    # Templates
    w(
        "templates/incorporation-checklist.md",
        """# NZ Incorporation Prep Checklist

DRAFT — NOT FOR SUBMISSION — founder files in own RealMe session.

- [ ] Decide legal name + 2 backups
- [ ] Confirm entity type (typically NZ limited company)
- [ ] Directors / shareholders details ready
- [ ] Registered office / address for service
- [ ] Share structure (note future ESOP gap if desired)
- [ ] Constitution vs Companies Act default — discuss with advisor if needed
- [ ] IRD number application plan
- [ ] GST registration decision (threshold / intent to trade)
- [ ] Business bank account requirements list
- [ ] Insurance quote list (if hardware on farms/worksites)
""",
    )
    w(
        "templates/annual-return-checklist.md",
        """# Annual Return / Records Checklist

INFORMATION ONLY — not a compliance certificate.

- [ ] Annual return due date on calendar
- [ ] Director / address details still correct
- [ ] Company records location known (Companies Act records)
- [ ] Ultimate holding company / share register updates noted
- [ ] Privacy Act — personal info inventory still accurate
""",
    )
    w(
        "templates/rdti-activity-log.csv",
        """date,hours,activity,technical_uncertainty,evidence_ref,person,notes
2026-07-14,2.0,Example — edge offline inference experiment,Model latency under offline constraint,commit:abc123,Founder,REPLACE with real rows — never invent
""",
    )
    w(
        "templates/grant-application-draft.md",
        """# DRAFT — NOT FOR SUBMISSION

- Opportunity:
- Project:
- Author skill: grants-rdti-clerk
- HITL required: YES

## Problem

## Solution

## Technical uncertainty / R&D character

## Method and milestones

## Risks

## Budget skeleton (placeholders only)

## Data sovereignty appendix

## Claims log
| Claim | VERIFIED / NEEDS_EVIDENCE | Source |

## Human submit checklist
- [ ] Figures verified
- [ ] Co-fund rules checked
- [ ] Cultural review if required
- [ ] Human submits via official portal
""",
    )
    w(
        "templates/market-validation-report.md",
        """# Market Validation Report

## Thesis

## Sizing (with sources)

## Competitors

## Pricing signals

## Interview guide

## Unknowns

## Confidence summary
""",
    )
    w(
        "templates/outreach-draft.md",
        """# DRAFT_NOT_SENT — Outreach

**UEM Act reminder:** Human must send. Confirm consent / existing relationship / compliance.

- To:
- Purpose:
- ICP segment:

## Subject

## Body

## Human send checklist
- [ ] Accurate identity
- [ ] Lawful basis / consent where required
- [ ] Unsubscribe / contact path if marketing
- [ ] No misleading claims
""",
    )
    w(
        "templates/gst-prep-checklist.md",
        """# GST Prep Worksheet

NOT A TAX FILING — human or accountant files in myIR.

- [ ] Period start / end
- [ ] Sales (GST inclusive/exclusive noted)
- [ ] Purchases with tax invoices
- [ ] Adjustments
- [ ] Working papers stored securely (not in public git)
""",
    )
    w(
        "templates/investor-data-room-index.md",
        """# Data Room Index (Prep)

NOT FINANCIAL ADVICE.

1. One-pager
2. Pitch deck
3. Product demo link / offline demo notes
4. Cap table (current)
5. Financial snapshot (high level)
6. Pilot LOIs / agreements (redacted as needed)
7. IP / ownership notes
8. Team
9. Risks
""",
    )
    w(
        "templates/nda-outline.md",
        """# NDA Outline — DRAFT — NOT LEGAL ADVICE

Sections to complete with lawyer:
1. Parties
2. Purpose
3. Definition of confidential information
4. Obligations
5. Exclusions
6. Term
7. Return/destruction
8. Governing law (New Zealand)
9. Signatures
""",
    )
    w(
        "templates/pilot-agreement-outline.md",
        """# Pilot Agreement Outline — DRAFT — NOT LEGAL ADVICE

1. Parties and champions
2. Pilot scope and sites
3. Term (e.g. 90 days)
4. Fees (paid pilots preferred)
5. Success criteria
6. Data ownership and residency
7. IP
8. Confidentiality
9. Liability / insurance
10. Conversion pricing path (optional pre-agreed)
11. Governing law NZ
12. Signatures
""",
    )
    w(
        "templates/privacy-policy-outline.md",
        """# Privacy Policy Outline — DRAFT — NOT LEGAL ADVICE

Align with Privacy Act 2020 IPPs:
1. Who we are
2. What we collect
3. Why we collect
4. How we collect
5. Storage and security
6. Access and correction
7. Sharing and overseas disclosure
8. Retention
9. Contact / complaints (OPC)
""",
    )
    w(
        "templates/employment-offer-outline.md",
        """# Employment Offer Outline — DRAFT — NOT LEGAL ADVICE

Use Employment NZ resources; lawyer/ER specialist for final:
1. Role title and duties
2. Location / hybrid
3. Hours
4. Remuneration
5. Leave
6. Trial period rules (current law — verify)
7. Confidentiality / IP
8. Health and safety
9. Start date
""",
    )
    w(
        "templates/weekly-operating-review.md",
        """# Weekly Operating Review — {{date}}

Prepared by: board-chief-of-staff  
Classification: Gold workflow + Platinum memory  
Status: DRAFT for human decision

## Snapshot
| Area | Status | Notes |
|------|--------|-------|
| Pipeline vs plan | | |
| Cash vs runway | | |
| Compliance deadlines (14d) | | |
| RDTI log hygiene | | |
| Top risks | | |

## Top 3 priorities (proposed)

1.
2.
3.

## Specialist queue

| Skill | Task | HITL |
|-------|------|------|
| | | |

## Decisions needed from founder

-
""",
    )
    w(
        "templates/constitution-notes.md",
        """# Constitution Notes — DRAFT — NOT LEGAL ADVICE

Discuss with advisor:
- Default Companies Act constitution vs custom
- Director decision rules
- Share classes
- Pre-emptive rights
- Future ESOP headroom thinking (not a substitute for ESOP plan)
""",
    )

    # Example company memory
    w(
        "memory/example-company/profile.md",
        """# Example Company Profile

- Proposed name: Example Sovereign Labs Limited
- Trading name: Example Sovereign
- Entity type: NZ limited company (not yet incorporated)
- Region: Taranaki, Aotearoa New Zealand
- NZBN: pending
- Directors: Founder Name
- Wedge: Local-first AI tooling for NZ operators
- ICP: Regional operators and EDAs evaluating sovereign AI
- Cultural partnerships: none claimed
- Data residency: local-first default
""",
    )
    w(
        "memory/example-company/decisions.md",
        """# Decisions

- 2026-07-14 — Adopted NZ Start-Up in a Box fleet for internal dogfooding.
- 2026-07-14 — Autonomy ceiling confirmed: draft/prepare only; human files/sends/pays.
""",
    )
    w(
        "memory/example-company/calendar.md",
        """# Compliance Calendar

| Due | Item | Owner | Status |
|-----|------|-------|--------|
| TBD | Incorporate | Founder | planned |
| TBD | IRD / GST | Founder | planned |
| Weekly | Board review | board-chief-of-staff | recurring |
| Ongoing | RDTI activity log | grants-rdti-clerk | recurring |
""",
    )
    w(
        "memory/example-company/pipeline.md",
        """# Pipeline

| Account | Stage | Next step | Owner |
|---------|-------|-----------|-------|
| Example EDA | discovery | book intro | Founder |
""",
    )
    w(
        "memory/example-company/runway.md",
        """# Runway Snapshot

- As-of: 2026-07-14
- Monthly burn (placeholder): update with real numbers
- Runway months (placeholder): update with real numbers
- Alerts: none

Do not store bank credentials here.
""",
    )
    w(
        "memory/example-company/rdti-log.csv",
        """date,hours,activity,technical_uncertainty,evidence_ref,person,notes
2026-07-14,1.5,Designed agent fleet skill schema for NZ founder lifecycle,Skill routing and HITL enforcement under multi-agent cost constraints,repo:NZ-Start-Up,Founder,Example row
""",
    )
    w(
        "memory/example-company/audit.jsonl",
        """{"ts":"2026-07-14T00:00:00Z","actor":"human:founder","skill":"nz-startup-fleet","action":"bootstrap_example_memory","tier":"platinum","hitl_required":false,"hitl_status":"n/a","artefact_ref":"memory/example-company/","summary":"Initialised example company memory","risk_level":"low"}
""",
    )
    w(
        "memory/example-company/weekly/2026-07-14.md",
        """# Weekly Operating Review — 2026-07-14

## Snapshot
| Area | Status | Notes |
|------|--------|-------|
| Pipeline vs plan | early | Example EDA only |
| Cash vs runway | TBD | Fill real numbers |
| Compliance deadlines | pre-incorporation | Formation pack next |
| RDTI log hygiene | started | Example row present |

## Top 3 priorities
1. Complete formation pack drafts
2. Keep RDTI log contemporaneous
3. Book discovery conversations
""",
    )
    w(
        "memory/README.md",
        """# Company Memory

- `example-company/` — safe demo data committed to git
- `companies/` — runtime founder data (gitignored)

Copy example to start:

```bash
cp -r memory/example-company memory/companies/my-startup
```

See `knowledge/company-memory-schema.md`.
""",
    )

    print("scaffold complete")


if __name__ == "__main__":
    main()
