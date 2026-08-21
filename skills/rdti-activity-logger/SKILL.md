---
name: rdti-activity-logger
version: "1.0.0"
requires_hitl: true
description: Use when capturing, formatting, or reviewing contemporaneous R&D Tax Incentive (RDTI) evidence for Coastal Alpine Tech. Turns commits, timesheets, decision notes, and technical work into audit-ready activity log entries. Triggers include RDTI log, log RDTI activity, contemporaneous evidence, R&D activity record, RDTI timesheet, record today's R&D. Never invent activities; only record what is evidenced.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-21"
  maturity: Gold
  related: [grants-rdti-clerk, grants-agent, aether-git-workflow, cat-architectural-standards]
---

# RDTI Activity Logger

Production skill for creating contemporaneous, audit-ready R&D activity records that support New Zealand R&D Tax Incentive claims.

## Core Principles
- Contemporaneous only — record as close to the work as possible.
- Evidence-based — never invent hours, people, or technical content.
- Linked to actual artefacts (commit SHAs, PR numbers, file paths, meeting notes).
- Clear hypothesis / technical uncertainty / systematic investigation framing where appropriate.

## When to Activate
- End of day / end of week R&D logging.
- After a significant technical decision, experiment, or implementation.
- Preparing material for the grants-rdti-clerk or external accountant.
- User says “log this for RDTI”, “add to R&D log”, or similar.

## Process

### 1. Gather Evidence
Ask for or extract:
- Date(s) of activity
- People involved (founder, contractors, collaborators)
- Hours (or best estimate with confidence)
- Technical problem / hypothesis / uncertainty
- What was done (systematic investigation, design, testing, iteration)
- Artefacts produced (commits, PRs, designs, test results, node builds)
- Outcome / next technical step

### 2. Format Entry
Produce a structured entry:

```markdown
### RDTI Activity — YYYY-MM-DD
**Project / Core area:** [e.g. Edge AI inference optimisation / Mana Kai node telemetry]
**People:** [names + roles]
**Hours:** [X] (confidence: high/medium/low)
**Technical uncertainty / hypothesis:**
[Clear statement of what was not known or being tested]
**Systematic work performed:**
- ...
**Artefacts / evidence:**
- Commit / PR: ...
- Files / hardware: ...
**Outcome & next step:**
...
**Eligible activity category:** [core R&D / supporting / etc. — flag if uncertain]
```

### 3. HITL Gate
- Present the draft entry.
- Confirm hours and technical framing with the founder before appending to any permanent log.
- Never auto-write to a claimed RDTI register without explicit approval.

## Guardrails
- Do not inflate hours or invent technical content.
- Flag activities that may sit outside eligible R&D (pure commercial packaging, marketing, routine maintenance).
- Keep language factual and technical; avoid hype.
- Align with IRD RDTI guidance principles (systematic, investigative, technical risk).
