---
name: aether-skill-sprint
version: "1.1.0"
requires_hitl: true
description: Use when sprinting for new skills, harness improvements, context packing, or prompt patterns from external sources. Extracts high-value patterns from Karpathy LLM Council, Agent Skills open standard, and related harnesses, then maps them into the Aether/CAT skill chain via aether-skill-authoring. Default for skill and harness sprints. Triggers include skill sprint, extract skills value, harness sprint, bring council patterns here, apply agentskills patterns.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  maturity: Gold
  family: skill-meta
  related: [aether-skill-authoring, aether-skill-forge, aether-skill-composition, aether-skill-companions, aether-skill-eval, aether-eval-harness, skill-creator]
  side_effect_class: local-write
  min_hitl_level: L2
  network_posture: explicit-only
---

# Aether Skill Sprint (v1.1.0)

Import external skill/council/harness value into the CAT fleet.

## Process
1. Frame — target, sources, constraints (sovereignty, HITL, edge).
2. Extract — process, progressive disclosure, prompts, harness fields only. Never invent source content.
3. Map — CAT frontmatter (`name`, `version`, `requires_hitl`, `description`), harness contract, HITL gates.
4. Author — via `aether-skill-authoring`.
5. Verify — companions + optional `aether-skill-eval`.
6. HITL — Skill Sprint Report before commit/push.

## Required output
Skill Sprint Report with sources, patterns, proposed skills, anti-rationalization, verification evidence, companions, authoring plan.
