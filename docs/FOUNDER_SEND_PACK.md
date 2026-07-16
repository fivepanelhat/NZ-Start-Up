# Founder send pack - Super Grok session 3

**Date:** 2026-07-16  
**Status:** READY FOR HUMAN - nothing auto-sent  
**Company memory:** `coastal-alpine-tech` (local / gitignored)

---

## 1. Your job this week (order matters)

| # | Action | Owner | Due (suggested) |
|---|--------|-------|-----------------|
| 1 | Personalise and **send** VT outreach (or write "no-send" in decisions.md) | Founder | 2026-07-18 |
| 2 | Pick **one** 90-day wedge: Byte Size Kai **or** Front Line Whanau | Founder | 2026-07-19 |
| 3 | Film cold-start using `docs/COLD_START_FILM_RUNBOOK.md` | Founder | 2026-07-20 |
| 4 | Optional: book lawyer hour (`docs/LEGAL_REVIEW_CHECKLIST.md`) | Founder | Days 8-14 |

Agents prepared everything below. **You** send.

---

## 2. VT email draft (copy-paste, then personalise)

**To:** (your PowerUp / VT contact - you fill)  
**Subject:** Founder OS for Taranaki - paid pilot idea for PowerUp (Coastal Alpine Tech)

```text
Kia ora [Name],

I'm Wayne Roberts, founder of Coastal Alpine Tech (New Plymouth / Taranaki).
We're pre-seed, R&D since Aug 2025, building NZ Start-Up in a Box: a local-first
"digital employee" fleet for NZ founders (formation prep, RDTI logs, GST working
papers, board packs) with hard HITL ceilings - agents draft/prepare; humans
file/send/pay/sign.

I'm not claiming a partnership - seeking a short conversation about a paid pilot
cohort inside PowerUp (10-15 seats, 90 days, white-label "Founder OS for Taranaki",
anonymised partner report, data stays on founder machines).

Happy to do a 10-minute offline demo (status board + board pack + compliance gate).

Ngā mihi,
Wayne Roberts
Coastal Alpine Tech Limited
[phone]
[your email]
```

**Full kit:** `docs/VT_POWERUP_APPROACH.md`  
**Pilot offer zip (DRAFT_NOT_SENT):**  
`memory/companies/coastal-alpine-tech/commercial/pilots/pilot-offer-latest.zip`  
(OneDrive: `SuperGrok-Proceed-2026-07-16/pilot-offer-DRAFT_NOT_SENT.zip`)

After you send: log date in `memory/companies/coastal-alpine-tech/decisions.md` and mark task done.

---

## 3. Demo commands (if they book)

```bash
cd NZ-Start-Up
python -m nz_startup demo run --company demo-vt --partner "Venture Taranaki" --programme "PowerUp demo"
python -m nz_startup board pack demo-vt
python -m nz_startup compliance check
```

See `docs/EDA_DEMO_KIT.md`.

---

## 4. Evidence status (honest)

| Item | Status |
|------|--------|
| pytest / doctor / smoke / compliance | Green (session 3) |
| demo-vt | status 100 |
| skills pack | v1.8.3 zip + sha256 |
| CAT readiness score | **100** with **sample** bank/invoice/xero-offline dogfood - replace with real exports before accountant handoff |
| Byte Size Kai README | ASCII-clean (no funny fonts) |
| Front Line Whanau live | https://front-line-whanau.vercel.app HTTP 200 |
| VT partnership | **Not claimed** - seeking only |

---

## 5. Wedge choice (fill one)

- [ ] **A - Byte Size Kai** (agritech field / hardware path)  
- [ ] **B - Front Line Whanau** (live social product)  

Write the choice in `decisions.md`. Do not pitch five portals as equal.

---

## 6. Autonomy reminder

> Agents inform, draft, prepare, monitor, and remind.  
> Humans advise, sign, file, send, and pay.

UEM Act: no automated cold email from this product.
