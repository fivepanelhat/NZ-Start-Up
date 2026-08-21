---
name: funding-council
version: "1.0.0"
requires_hitl: true
description: Use when pressure-testing funding, grant, ScaleUp, RDTI, capital allocation, or investor-related decisions. Specialised instance of the decision-council pattern with five lenses tuned for non-dilutive and early-stage capital choices. Triggers include funding council, grant council, ScaleUp decision, RDTI positioning, capital allocation, should we apply for, funding trade-off, investor terms review. Always apply for genuine uncertainty with material capital or dilution stakes.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-21"
  maturity: Gold
  related: [aether-decision-council, grants-agent, grants-rdti-clerk, funding-analyst, investor-readiness-clerk]
---

# Funding Council

Specialised Coastal Alpine Tech decision council for funding, grants, RDTI, and early capital decisions. Re-uses the proven five-lens + anonymous peer-review + chairman synthesis pattern with funding-specific framing.

## When to Activate
- Deciding whether / how to apply for a specific grant or ScaleUp.
- Choosing between non-dilutive paths vs early equity conversations.
- Pressure-testing RDTI positioning or claim framing.
- Reviewing draft investor or SAFE terms before engagement.
- Any capital allocation decision with material opportunity cost.

## Process (inherits aether-decision-council structure)

### 1. Frame & Enrich
Restate the funding decision neutrally. Pull relevant context: current runway, existing applications, RDTI status, dilution preferences, strategic fit with CAT sovereignty and edge focus.

### 2. Five Advisors (Funding-tuned lenses)
1. **The Contrarian** — hunts hidden costs, reporting burden, strategic distraction, and reasons not to pursue.
2. **The First-Principles Thinker** — strips grant language and asks what actual technical or commercial progress is being bought.
3. **The Expansionist** — surfaces optionality, follow-on funding potential, and network effects from the funder relationship.
4. **The Outsider** — views the opportunity with zero loyalty to “we should apply for everything” bias.
5. **The Executor** — demands the concrete Monday-morning actions, evidence requirements, and realistic timeline.

### 3. Anonymous Peer Review + Chairman Synthesis
Same structure as aether-decision-council. Chairman must explicitly surface:
- Dilution vs non-dilutive trade-offs
- Reporting / compliance burden
- Strategic fit with sovereign edge and Te Mana Raraunga posture
- Recommended next action and confidence

### 4. HITL Gate
Any recommendation that commits the company to an application, changes capital strategy, or involves external investor conversations requires explicit founder approval before action.

## Output
Use the standard Council Verdict structure, with an additional **Capital & Dilution Notes** section.
