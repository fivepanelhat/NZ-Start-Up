---
name: cultural-safety-gate
version: "1.0.0"
requires_hitl: true
description: Use whenever content, decisions, data handling, or public statements may touch Māori data, iwi, mana whenua, Te Tiriti principles, Mana Kai, whānau, or cultural narratives. Runs an explicit Te Mana Raraunga and Te Tiriti alignment checklist and forces a human / cultural review gate before proceeding. Triggers include cultural review, Te Mana Raraunga check, iwi content, mana whenua, cultural safety, Te Tiriti alignment, Māori data, whānau facing content. Always escalate rather than assume.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-21"
  maturity: Gold
  related: [te-mana-raraunga-controls, aether-data-sovereignty, aether-hitl-protocol, aether-core]
---

# Cultural Safety Gate

Mandatory review and escalation skill for any work that intersects Māori data sovereignty, Te Tiriti o Waitangi principles, iwi/mana whenua relationships, or culturally sensitive content.

## When to Activate (Mandatory Triggers)
- Any public or partner-facing text that mentions iwi, mana whenua, Te Tiriti, or Māori data.
- Data models, consent flows, or storage decisions involving Māori or community data.
- Mana Kai / farm / whenua related features that could affect collective benefit or rangatiratanga.
- Grant or funding narratives that claim cultural alignment or partnership.
- Any uncertainty about whether cultural review is required → activate this skill.

## Checklist (Must Complete)

### 1. Rangatiratanga (Authority & Control)
- Who owns / controls the data or narrative?
- Is authority being retained by the appropriate people or entities?

### 2. Whakapapa (Relationships & Context)
- Are relationships, history, and context being respected or erased?
- Is the content extracting value without reciprocal relationship?

### 3. Manaakitanga (Care & Reciprocity)
- Does the work care for people and relationships, or only extract utility?
- Are benefits flowing back to the communities involved?

### 4. Kaitiakitanga (Guardianship)
- Is the data or taonga being protected for future generations?
- Are there clear safeguards against misuse or unintended exposure?

### 5. Kotahitanga (Collective Benefit)
- Does the work support collective outcomes rather than purely individual or commercial gain?

### 6. Practical Data Controls
- Local processing / owner-controlled keys where required?
- Explicit consent and ability to withdraw?
- No silent exfiltration?

## Process
1. Run the checklist against the proposed content or decision.
2. Produce a short Cultural Safety Assessment:
   - Items that pass
   - Items that need strengthening
   - Items that require external cultural / iwi advisory input
3. **HITL / Escalation Gate**
   - Present the assessment.
   - Do not proceed to public release, partner send, or production deployment until explicit human (and where indicated cultural) approval is given.
   - Default posture: escalate rather than assume safety.

## Guardrails
- Never claim iwi partnership or endorsement without evidence.
- Never treat cultural review as a checkbox that can be skipped under time pressure.
- When in doubt, stop and escalate.
