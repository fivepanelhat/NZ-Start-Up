---
name: cat-doctor
version: "1.0.0"
requires_hitl: false
description: Use when checking Coastal Alpine Tech edge node health — Raspberry Pi 5, Hailo NPU, sensors, local Ollama, network, and Core stack readiness. Triggers include cat doctor, edge health check, RPi health, Hailo status, node doctor, is the node ready, pre-flight edge.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  maturity: Gold
  family: domain-vertical
  related: [edge-node-commissioning, kiwi-edge-architecture, cat-model-sentinel, cat-egress-sentinel, aether-skill-companions]
  side_effect_class: read-only
  min_hitl_level: L1
  network_posture: explicit-only
  resource_envelope: light
---

# CAT Doctor

Edge health report: host, Hailo, models, connectivity/egress, Core stack, sensors. Read-only probes. Flag unexpected egress. Pair with edge-node-commissioning for first-time sign-off.
