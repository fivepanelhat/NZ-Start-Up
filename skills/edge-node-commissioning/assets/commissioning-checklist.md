# Edge Node Commissioning Checklist

**Node ID:**  
**Site / Farm:**  
**Date started:**  
**Commissioner:**

## Phase 0 — Pre-flight
- [ ] Hardware inventory recorded (serials)
- [ ] Intended location & data owner confirmed
- [ ] Sovereignty requirements noted

## Phase 1 — Base OS & Hardware
- [ ] OS image verified and booted
- [ ] Memory / storage / thermal OK
- [ ] Hailo runtime installed
- [ ] Hailo smoke inference passed

## Phase 2 — Core Software
- [ ] Coastal-Alpine-Core installed
- [ ] SovereignOllamaClient + model OK
- [ ] MQTT / mTLS (if required) verified
- [ ] SecurityGuard baseline green

## Phase 3 — Domain & Sensors
- [ ] Sensors attached and reading
- [ ] Domain loop / portal functional
- [ ] End-to-end local data path tested

## Phase 4 — Sovereignty & Hardening
- [ ] No unexpected outbound connections
- [ ] Local credential / key handling verified
- [ ] Logging & retention policy set
- [ ] Access controls documented

## Phase 5 — Sign-off
- [ ] Commissioning report generated
- [ ] Human production-ready approval obtained
- [ ] Node registered in operations log

**Production-ready sign-off**  
Name: ________________  Date: ________  Signature / confirmation: ________
