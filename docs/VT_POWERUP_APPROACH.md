# Venture Taranaki PowerUp - Approach Kit

**Coastal Alpine Tech Limited | Pre-seed | Taranaki**
Prepared 2026-07-15 | Status: **DRAFT_NOT_SENT** - human reviews, personalises, and sends.
Evidence base: [`docs/MARKET.md`](./MARKET.md) | [`knowledge/agentic-ecosystem-nz.md`](../knowledge/agentic-ecosystem-nz.md) | [`docs/WHITE_LABEL.md`](./WHITE_LABEL.md) | [`docs/EDA_DEMO_KIT.md`](./EDA_DEMO_KIT.md) | [`docs/OPTIMIZATION_EXECUTION.md`](./OPTIMIZATION_EXECUTION.md)

> House rules apply: UEM Act - humans send. No over-claims - every line below is "seeking collaboration", never "in partnership with". Cultural content stays HITL.

---

## 1. The one-pager (hand this over)

### Founder OS for Taranaki - white-label for PowerUp

**What it is.** *NZ Start-Up in a Box* - a local-first digital-employee fleet for NZ founders: formation prep, GST working papers, RDTI contemporaneous logging, grants radar, pipeline hygiene, and one-command board packs. Agents draft and prepare; **humans file, send, pay, and sign** - hard-coded, not a policy promise.

**Why Venture Taranaki.** We are a Taranaki pre-seed company (R&D since Aug 2025, founded Aug 2026, six generations of whanau agriculture behind us). PowerUp cohorts are exactly our P0 segment: ~90% of NZ enterprises have fewer than 10 people, and the tracked startup ecosystem grew +26% last year while only 47 new companies got first funding - founders must be capital-efficient, and admin is where their week goes. (Full verified stats: `docs/MARKET.md`.)

**What a PowerUp cohort gets.**

| For each founder | For Venture Taranaki |
|------------------|----------------------|
| Pre-seeded company memory + 30-day plan on day one | Branded white-label pack ("Founder OS for Taranaki") |
| Xero read-only + bank CSV finance clerk from week one | Cohort readiness report, anonymised on request |
| RDTI activity logging that makes claims defensible | Zero PII in partner exports - seat data stays on founder machines |
| Board pack in one command for mentor sessions | Per-seat licensing, no multi-tenant SaaS risk |
| Hard legal ceilings (UEM, Privacy Act, FMCA flags) | A Taranaki-built product to showcase - regional story included |

**What it is not.** Not autonomous agents sending email on founders' behalf. Not offshore-default data practice. Not open source - dual-licensed NZ IP.

**The ask.** One pilot cohort (10-15 seats) inside an upcoming PowerUp intake, paid per-seat, 90 days, with a named champion and pre-agreed go/no-go criteria. We run the onboarding; founders keep their data.

**Differentiator worth saying out loud.** As of July 2026 no public NZ player combines a productised installable agent fleet with hard HITL, NZ jurisdiction depth, Te Mana Raraunga alignment, and white-label EDA packaging - the nearest neighbours are service-model agent shops and enterprise consultancies. Even our market claims are freshness-gated: the stats behind this page fail our CI build if they go 90 days without re-verification.

---

## 2. Live demo runbook (10 minutes, offline-capable)

Run in order; everything works without cloud credentials:

```bash
# 1. Full EDA demo - init, pipeline, grants, Xero snapshot, bank import,
# GST papers, invoice triage, handoff zip, weekly board (~3 min)
nz-startup demo run --company demo-vt --partner "Venture Taranaki" --programme "PowerUp demo"

# 2. Show the founder-facing outputs
nz-startup status demo-vt # readiness score
nz-startup board pack demo-vt # mentor-ready zip

# 3. Show the cohort machinery (the white-label story)
nz-startup cohort init vt-powerup --partner "Venture Taranaki" --programme "PowerUp" --quota 15 --tagline "Founder OS for Taranaki"
nz-startup cohort add-seat vt-powerup --founder demo --company demo-vt --name "Demo Founder"
nz-startup cohort report vt-powerup --anonymise # what VT would receive
nz-startup cohort pack vt-powerup # white-label zip, no PII

# 4. Close on trust: the ceilings are code, not slides
nz-startup compliance check
```

Talking points while it runs: seat data never leaves the founder's machine; the partner report is anonymised by default; the compliance gate is the same one CI runs on every commit.

---

## 3. Outreach email - DRAFT_NOT_SENT

**UEM Act checklist before sending:** existing relationship or lawful basis confirmed | accurate sender identity | contact/unsubscribe path | no misleading claims | personalise the bracketed fields.

> **To:** [named PowerUp / Venture Taranaki contact - no cold generic inbox]
> **Subject:** Taranaki-built founder OS - pilot cohort offer for PowerUp
>
> Kia ora [name],
>
> I'm Wayne Roberts - Coastal Alpine Tech, a pre-seed venture here in Taranaki (whanau six generations in agriculture locally). We've built *NZ Start-Up in a Box*: a local-first digital-employee fleet that takes formation prep, GST working papers, RDTI logging, grants tracking, and board packs off a founder's plate - with humans always doing the filing, sending, paying, and signing.
>
> It's built to be white-labelled for exactly a PowerUp-shaped cohort: each founder gets a pre-seeded company workspace on day one, you get an anonymised cohort readiness report, and no founder data ever touches our servers - it stays on their machines.
>
> I'd like to offer a paid pilot: 10-15 seats inside an upcoming intake, 90 days, clear go/no-go criteria agreed up front. I can demo the full flow offline in 10 minutes, whenever suits - your office or ours.
>
> Would a short call in the next fortnight work?
>
> Nga mihi,
> Wayne Roberts
> Coastal Alpine Tech Limited | Taranaki
> [phone] | [email]

---

## 4. Anticipated questions (crib sheet)

| They ask | We say |
|----------|--------|
| "Is this ChatGPT with extra steps?" | No API key needed for core value; jurisdiction depth (RDTI/GST/UEM/Privacy Act) is the product, and autonomy ceilings are enforced in code - `nz-startup compliance check` shows all 23 gates. |
| "What happens to founder data?" | Local-first on the founder's machine. Partner reports are aggregate and anonymisable. Te Mana Raraunga alignment documented in `compliance/te-mana-raraunga.md`. |
| "What does it cost?" | Founder ~$49/mo | Active ~$149/mo | cohort seats ~$399/mo with white-label branding and partner reporting. Pilot pricing negotiable against a signed go/no-go. |
| "Who else uses it?" | Honest answer: pre-seed, dogfooded on Coastal Alpine Tech itself with full RDTI logging. That's why we want PowerUp as the first cohort - and why it's a paid pilot, not a promise. |
| "Maori data / cultural content?" | Hard HITL: cultural sensitivity flags gate any iwi/whenua-facing output to human + cultural review. We don't do extractive branding. |
| "Why not [global AI tool]?" | Nothing global ships NZ legal ceilings, RDTI contemporaneous evidence, or EDA white-label packs. Ecosystem map with sources: `knowledge/agentic-ecosystem-nz.md`. |

---

## 5. Follow-through sequence

1. **Before contact:** personalise the draft, confirm the named contact, run the demo end-to-end once on the presenting machine.
2. **After a yes to a call:** send the one-pager (section 1) as PDF; nothing else.
3. **After the demo:** `nz-startup pilot offer` with the agreed seats/fee/criteria -> offer zip -> human sends and signs.
4. **After a signed pilot:** `cohort init` for real, log every build hour to RDTI, schedule the 90-day partner report.
5. **If no:** ask what would change the answer, log it in pipeline, revisit next intake. No drip campaigns - one follow-up maximum, then park it.
