---
name: cat-prompt-registry
version: "1.0.0"
requires_hitl: true
description: Use when creating, versioning, evaluating, or securing system prompts and skill prompts across CAT repos. Treats prompts as code with registry, golden tests, and injection-corpus hooks. Triggers include prompt registry, version this prompt, prompt as code, golden prompt test, prompt injection corpus.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  maturity: Gold
  family: skill-meta
  related: [aether-skill-authoring, aether-eval-harness, aether-skill-eval, agent-hardening, aether-skills-ci, aether-skill-companions]
  side_effect_class: local-write
  min_hitl_level: L2
  network_posture: none
---

# CAT Prompt Registry

Prompts-as-code. Layout: prompts/system, skills, few-shot, injection-corpus, evals. Branch any change; require golden case; run injection smoke for untrusted input; HITL before merge for customer-facing agents. No secrets in prompts.
