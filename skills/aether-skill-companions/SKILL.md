---
name: aether-skill-companions
version: "1.0.0"
requires_hitl: false
description: Use whenever skills are selected, composed, authored, or executed on non-trivial work. Maintains the skill-family knowledge base and automatically proposes companion skills to load with the primary skill. Triggers include companions, skill family, related skills, what else should load, companion lookup, auto companions, skill graph.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  maturity: Gold
  family: skill-meta
  related: [aether-skill-composition, aether-skill-authoring, aether-skill-sprint, aether-skill-forge, aether-core, cat-architectural-standards, aether-hitl-protocol]
  side_effect_class: read-only
  min_hitl_level: L1
  network_posture: none
---

# Aether Skill Companions (v1.0.0)

Automatic companion discovery for the Aether/CAT fleet.

1. Identify primary skill(s).
2. Look up family + edges in `references/skill-families.md`.
3. Propose 1–4 companions with role and load level (metadata vs full).
4. Always layer global safety stack for significant or sovereignty work.
5. When new skills are authored, update skill-families.md in the same change set.

Global always-consider: aether-core, cat-architectural-standards; plus te-mana-raraunga-controls, aether-data-sovereignty, aether-hitl-protocol for sovereignty/cultural/data work.
