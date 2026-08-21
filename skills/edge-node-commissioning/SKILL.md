---
name: edge-node-commissioning
version: "1.0.0"
requires_hitl: true
description: Use when bringing up, validating, or documenting a Coastal Alpine Tech edge node (RPi 5 16GB + Hailo-10H + sensors + local Ollama). Provides phased commissioning checklist, hardware validation, software stack bring-up, security hardening, and Te Mana Raraunga local-data checks. Triggers include commission node, bring up RPi, Mata Kai node, edge node setup, Hailo validation, node commissioning, farm node install. Always require human confirmation before marking a node production-ready.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-21"
  maturity: Gold
  related: [cat-architectural-standards, aether-data-sovereignty, te-mana-raraunga-controls, coastal-alpine-core]
---

# Edge Node Commissioning

Production skill for repeatable, sovereign commissioning of Kiwi Edge nodes (Raspberry Pi 5 16GB + Hailo-10H NPU + sensor suite + local LLM).

## Target Hardware Baseline
- Raspberry Pi 5 (16GB recommended)
- Hailo-10H M.2 / AI HAT
- Official or high-quality power supply
- Storage (NVMe or high-endurance SD)
- Network (Ethernet preferred for field stability)
- Sensors as required by domain portal (AquaGuard, SoilGuard, Mata Kai, etc.)

## Phased Process

### Phase 0 — Pre-flight
- Confirm physical inventory and serial numbers
- Record intended site / farm / Mana Kai location
- Confirm data-sovereignty requirements for this node

### Phase 1 — Base OS & Hardware
- Flash and boot verified OS image
- Confirm CPU, memory, storage, thermal
- Install and validate Hailo runtime + firmware
- Run Hailo basic inference smoke test

### Phase 2 — Core Software Stack
- Install / update Coastal-Alpine-Core
- Configure SovereignOllamaClient + local model(s)
- Bring up MQTT / mTLS if required
- SecurityGuard baseline checks

### Phase 3 — Domain & Sensors
- Attach and validate sensors
- Configure domain portal or agent loop
- End-to-end data path test (sensor → local process → optional flywheel)

### Phase 4 — Sovereignty & Hardening
- Confirm no unexpected outbound data paths
- Local key / credential handling verified
- Logging and telemetry retention policy set
- Physical and network access controls documented

### Phase 5 — Sign-off
- Produce commissioning report
- Human (founder or authorised operator) signs off “production-ready”
- Record node ID, location, software versions, and next maintenance window

## HITL Gates
- Before declaring any node production-ready.
- Before enabling any data path that could leave the local site.
- Before changing security or key-management configuration.

## Output
Structured commissioning checklist + final sign-off report in markdown, ready for the node register / operations log.
