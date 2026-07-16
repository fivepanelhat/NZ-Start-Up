# EDA / Venture Taranaki demo kit

**Status:** Internal kit · **DRAFT materials only** · humans send all outreach.  
**Sources:** Claude reports #8 (final review), #10 (NZ stats/adoption), #11 (agentic collab map), #9 (one-liner).

---

## 1. Global one-liner (use consistently)

> Coastal Alpine Tech is building the sovereign hybrid edge-AI stack for Aotearoa's primary industries and founders — local-first RPi 5 + Hailo nodes, multi-model fleets (Grok/Claude/Gemini), Te Mana Raraunga data sovereignty, and white-label EDA tools — actively seeking collaboration with Venture Taranaki, startups.com investors, and the Kotahitanga Investment Fund to scale intergenerational Maori and regional economic outcomes.

**Guardrails:** no implied existing deals · HITL + cultural advisory for any formal Maori-data approach.

---

## 2. ICP facts (re-verify before external decks)

| Fact | Figure | Caveat |
|------|--------|--------|
| NZ enterprises | ~617k | Stats NZ Feb 2025 |
| Zero-employee share | ~74% | Primary digital-employee ICP |
| Tracked startups | ~764–2400 | Definition-dependent |
| 2025 NZ investment | $754m / 166 deals | NZGCP; only 47 new first-checks |
| Target segment | 0–10 people | ~90% of enterprises under 10 |

Full synthesis: Downloads `10-nz-startups-deep-dive-and-adoption-report.md` and in-repo `docs/MARKET.md` if present.

---

## 3. Why white space (Claude #11)

- No public VT / startups.com / Kotahitanga collab with a fleet of this depth (as of report date).  
- Nearby players: AgentWorks (service), AgenticLabs (consultancy), Arcanum+Grant Thornton (enterprise) — different ICP.  
- **Fastest entry:** Venture Taranaki PowerUp white-label pilot (10–15 seats, 90 days).

---

## 4. Offline demo (10 minutes)

```bash
nz-startup doctor
nz-startup demo run --company demo-vt --partner "Venture Taranaki" --programme "PowerUp demo"
nz-startup status demo-vt
nz-startup board pack demo-vt
nz-startup cohort init vt-powerup --partner "Venture Taranaki" --programme "PowerUp" --quota 15 --tagline "Founder OS for Taranaki"
nz-startup cohort add-seat vt-powerup --founder demo --company demo-vt --name "Demo Founder"
nz-startup cohort report vt-powerup --anonymise
nz-startup compliance check
```

Talking points:

1. Jurisdiction depth is the moat (RDTI, GST papers, grants) — not agent hype.  
2. Autonomy ceiling is code: draft/prepare only.  
3. Seat data stays on founder machines; partner report anonymised.  
4. Paid pilot only — free pilots do not convert.

---

## 5. Outreach

Full email draft + UEM checklist: [`VT_POWERUP_APPROACH.md`](./VT_POWERUP_APPROACH.md)  
**Status: DRAFT_NOT_SENT** — do not auto-send.

---

## 6. Pricing (internal, Claude #10)

| Tier | Indicative NZD/mo | Role |
|------|-------------------|------|
| Founder | ~$49 | Solo / micro |
| Active | ~$149 | Early team |
| Cohort seat | ~$399 | EDA white-label |

Not published commercial terms until commercial track / pilot offer is signed.
