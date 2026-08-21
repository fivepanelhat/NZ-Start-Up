---
name: pilot-loi-drafter
version: "1.0.0"
requires_hitl: true
description: Use when drafting, refining, or reviewing a pilot Letter of Intent (LOI), pilot agreement outline, or conversion-ready term sheet for Coastal Alpine Tech edge / AgriTech / Mana Kai deployments. Produces structured LOIs with clear success metrics, Te Mana Raraunga data clauses, pricing conversion path, duration, and HITL approval gates. Triggers include pilot LOI, draft LOI, letter of intent, pilot terms, conversion pricing, pilot agreement, LOI for farm, LOI for EDA. Always require human review before any external send.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-21"
  maturity: Gold
  related: [aether-decision-council, nz-startup-partnership, te-mana-raraunga-controls, cat-architectural-standards]
---

# Pilot LOI Drafter

Coastal Alpine Tech production skill for generating high-quality, sovereign-aligned pilot Letters of Intent.

## When to Activate
- User asks to draft, revise, or pressure-test a pilot LOI or term sheet.
- Preparing material for farm, EDA, council, or iwi pilot discussions.
- Converting a successful discovery conversation into a written LOI.

## Core Process

### 1. Capture Context
- Counterparty type (farm / EDA / council / iwi entity / other).
- Scope of pilot (nodes, sensors, domain portal, duration).
- Desired outcomes and success metrics.
- Any commercial constraints already discussed (pricing, exclusivity, data ownership).
- Cultural or Te Mana Raraunga sensitivities.

### 2. Draft Structure (Mandatory Sections)
Produce a clean markdown LOI containing at minimum:

1. **Parties**
2. **Purpose & Scope**
3. **Pilot Duration & Milestones**
4. **Success Metrics** (measurable, time-bound)
5. **Data & Sovereignty Clauses** (explicit Te Mana Raraunga alignment, local processing, owner-controlled keys, no silent exfiltration)
6. **Commercial Framework** (pilot pricing or fee structure + clear conversion path to paid subscription / HaaS / PaaS)
7. **Roles & Responsibilities**
8. **Confidentiality & IP**
9. **Termination & Next Steps**
10. **Signatures / Approval**

### 3. HITL Gate
Before treating any draft as final or ready to send:
- Present the full LOI.
- Explicitly flag any cultural, data-sovereignty, or pricing items that require founder or cultural advisory review.
- Ask: “Ready to send externally, needs edits, or require cultural / legal review first?”

## Guardrails
- Never invent traction, revenue, or existing partnerships.
- Never weaken data-sovereignty language.
- Keep language commercial but non-binding where appropriate for an LOI.
- Flag if the counterparty is mana whenua or involves Māori data — escalate cultural review.

## Output
Return the LOI in clean markdown ready for copy into Google Docs / Word / email, plus a short “Notes for Founder” section listing open questions and recommended next actions.
