# Seed investor pack - Coastal Alpine Tech / NZ Start-Up in a Box

**Status:** DRAFT for founder personalisation | **Not a prospectus | Not an offer of securities** 
**Date:** 2026-07-15 | **Product version:** 1.8.0 
**Company:** Coastal Alpine Tech Limited (pre-seed) | Taranaki, Aotearoa New Zealand

---

## 1. Why this is investable now

| Pillar | Proof (verify in repo / Drive) |
|--------|--------------------------------|
| **Real product, not a deck** | Installable CLI + MCP + console; 90+ automated tests; CI runs doctor/compliance/smoke/evals |
| **Hard legal ceilings** | HITL default-deny in code; no send/file/pay tools on MCP surface |
| **NZ jurisdiction moat** | RDTI, GST papers, Privacy Act, UEM flags, Te Mana Raraunga |
| **Market wedge with data** | 617k NZ enterprises; ~90% <10 staff; only 47 first-funded in 2025 -> admin OS demand |
| **Clear first customer** | Venture Taranaki PowerUp white-label pilot kit ready (`docs/VT_POWERUP_APPROACH.md`) |
| **R&D continuity** | Claimed R&D since **8 Aug 2025** mapped to Drive artefacts + this product (`docs/INVESTOR_RD_AND_MARKET_REFERENCE.md`) |
| **Portfolio optionality** | Edge agritech stack (Byte Size Kai, SoilGuard, Sting...) as expansion - see portfolio matrix |
| **IP posture** | Dual proprietary + commercial licence (NZ Copyright Act 1994) |

---

## 2. The product (10 seconds)

**NZ Start-Up in a Box** - local-first digital employees for NZ founders:

- Formation prep, finance triage, grants/RDTI, pipeline, board packs 
- White-label for EDAs (cohort seats + anonymised partner reports) 
- Agents **draft and prepare**; humans **file, send, pay, sign**

```bash
pip install -e ".[all]"
nz-startup doctor && nz-startup smoke
nz-startup demo run --company demo-vt --partner "Venture Taranaki"
```

---

## 3. Market (honest bottom-up)

| Layer | Size | Note |
|-------|------|------|
| SOM | EDA cohorts + early founders | PowerUp-class seats first |
| SAM | ~101k micro-enterprises (1-5) + growth zeros | Only growth-oriented fraction |
| TAM ceiling | ~557k enterprises 0-5 staff | Ceiling, not demand |

Full matrix: [`docs/MARKET_FIT_MATRIX.md`](./MARKET_FIT_MATRIX.md) | stats: [`docs/MARKET.md`](./MARKET.md)

---

## 4. Traction & readiness (as of July 2026)

| Signal | State |
|--------|-------|
| Engineering | v1.8.x fleet ops + trust-transfer + market intelligence |
| Commercial | Pilot offer packs, cohort machinery, VT approach kit (**DRAFT_NOT_SENT**) |
| Customers | Pre-seed - pilot LOIs are the next milestone (do not invent) |
| Dogfood | Coastal Alpine Tech company memory + RDTI logging path |
| Compliance collateral | OWASP/NIST/ISO mapping, dual licence, SECURITY contact |

---

## 5. Use of funds (indicative seed)

| Bucket | Share | Outcome |
|--------|-------|---------|
| EDA pilot + founder GTM | 40% | First paid seats, case study |
| Edge agritech pilot | 25% | One field vertical proof |
| Hardening / SecOps | 15% | Enterprise DD readiness |
| Legal / IP / incorporation / RDTI | 10% | Clean cap table & claims |
| Cultural advisory / impact | 10% | Gated pathways done properly |

---

## 6. Risks (say them first)

1. **Key-person** - solo founder technical depth; mitigate with docs, dual licence, hire plan 
2. **Commercialisation** - product ahead of sales; mitigate with VT pilot kit and paid pilots only 
3. **Overclaim risk** - valuation memos in Drive are working papers, not audited; we lead with **verifiable product** 
4. **Enterprise sales cycle** - we do **not** chase 100+ headcount as beachhead 

---

## 7. The ask (template - founder fills numbers)

> Seeking **NZ$___ pre-seed** on a **SAFE / equity** (terms TBD) to fund a **90-day Venture Taranaki cohort pilot**, first **paid founder seats**, and **one agritech edge pilot**, with RDTI logging and dual-licence IP protection already in place.

Collaboration intent (not existing deals): Venture Taranaki | startups.com investors | Kotahitanga Investment Fund (cultural HITL for formal approach).

---

## 8. Data room index (point diligence here)

| Item | Location |
|------|----------|
| Product source | github.com/fivepanelhat/NZ-Start-Up |
| R&D chronology | `docs/INVESTOR_RD_AND_MARKET_REFERENCE.md` |
| Market + ICP | `docs/MARKET.md`, `docs/MARKET_FIT_MATRIX.md` |
| Portfolio | `docs/PORTFOLIO_MARKET_FIT.md` |
| VT approach | `docs/VT_POWERUP_APPROACH.md` |
| Licence | `LICENSE`, `LICENSE-COMMERCIAL.md`, `docs/DUAL_LICENCE.md` |
| Controls | `compliance/standards-mapping.md`, `COMPLIANCE.md` |
| Architecture | `docs/ARCHITECTURE.md`, `docs/STANDARDS.md` |
| Security | `SECURITY.md` |

Generate refreshed index:

```bash
nz-startup investor data-room --company coastal-alpine-tech
```

---

## 9. Demo for investors (8 minutes)

1. `nz-startup about` - dates, one-liner, hybrid 
2. `nz-startup demo run` - offline EDA path 
3. `nz-startup compliance check` - control plane 
4. `nz-startup market matrix` - who pays first 
5. Open `docs/SEED_INVESTOR_PACK.md` + VT kit 

---

*Humans send this pack. Agents only draft. Coastal Alpine Tech Limited | Taranaki.*
