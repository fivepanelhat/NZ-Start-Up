---
name: cat-decision-log
version: "1.0.0"
requires_hitl: true
description: Use when recording or designing the immutable log of high-stakes HITL decisions (actuator control, grant filing, data export, capital commitments, cultural releases). Triggers include decision log, log this decision, HITL decision registry, record approval, immutable decision, decision audit trail.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  maturity: Gold
  family: cat-governance
  related: [aether-hitl-protocol, aether-core, cat-architectural-standards, aether-data-sovereignty, te-mana-raraunga-controls, aether-skill-companions]
  side_effect_class: local-write
  min_hitl_level: L2
  network_posture: none
  sovereignty_notes: Decision records stay under owner-controlled storage; no silent exfiltration.
---

# CAT Decision Log

Append-only local-first registry for high-stakes HITL decisions. Agents draft; humans set final outcome. Force HITL if confidence < 0.8. Schema includes ID, domain, action, evidence, confidence, rationale, risk flags, outcome, approver, conditions, follow-ups.
