# 10-minute EDA / VT demo script

**Audience:** Venture Taranaki / PowerUp-style programme staff  
**Mode:** Offline-capable laptop demo  
**HITL close:** "We did not email anyone in this demo."

---

## Minute 0-1 - Frame

- Coastal Alpine Tech: Taranaki pre-seed, founder OS + sovereign edge stack.  
- Product for this room: **NZ Start-Up in a Box** (white-label for cohorts).  
- Seeking **paid pilot conversation**, not claiming partnership.

## Minute 1-4 - Live run

```bash
python -m nz_startup demo run --company demo-vt --partner "Venture Taranaki" --programme "PowerUp demo"
```

Show talking points from the printed demo report (jurisdiction depth, HITL ceilings, board pack).

## Minute 4-6 - Board pack + score

```bash
python -m nz_startup status demo-vt
python -m nz_startup board pack demo-vt
```

Open `board-packs/board-pack-latest.zip` - mentor artefact.

## Minute 6-8 - Trust

```bash
python -m nz_startup compliance check
python -m nz_startup harden status
```

Point: forbidden tools / send-file-pay blocked in code, not slideware.

## Minute 8-10 - Ask

- One pilot cohort: 10-15 seats, 90 days, paid per seat.  
- VT gets: anonymised readiness report + white-label brand pack.  
- Founders keep data on their machines.  
- Next step: named champion + go/no-go criteria.

**Leave-behind:** pilot offer DRAFT zip (human emails after call).

---

## Props checklist

- [ ] Python env pre-warmed (`doctor` PASS)  
- [ ] demo-vt already smoked once  
- [ ] Screen zoom 125%  
- [ ] One-liner ready (no partnership claim)  
