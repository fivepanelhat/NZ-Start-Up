# Enterprise & segment market-fit matrix

**Product:** NZ Start-Up in a Box · Coastal Alpine Tech Limited · Pre-seed  
**Verified:** 2026-07-15 · **Version:** 1.8.0  
**Sources:** `docs/MARKET.md`, `knowledge/nz-market-stats.md`, `knowledge/agentic-ecosystem-nz.md`, `docs/INVESTOR_RD_AND_MARKET_REFERENCE.md`  
**CLI:** `nz-startup market matrix` · `nz-startup market score --segment <id>`

> Score legend (0–5 each dimension): **Problem** intensity · **Willingness to pay** · **CAT product fit** · **Sales cycle** speed (5 = fast) · **Trust / compliance** need met · **Taranaki/NZ impact**.  
> **Total** = sum (max 30). **Go** ≥ 22 · **Pilot** 16–21 · **Watch** 10–15 · **No** < 10.

---

## 1. Beachhead matrix (who buys *this* product)

| ID | Segment | Problem | WTP | Fit | Speed | Trust | NZ impact | **Total** | Decision | Entry motion | Primary skills |
|----|---------|---------|-----|-----|-------|-------|-----------|-----------|----------|--------------|----------------|
| **S1** | Solo / 1–3 person tech founders | 5 | 3 | 5 | 5 | 4 | 4 | **26** | **GO** | Direct install + freemium | formation, finance, grants-rdti, board |
| **S2** | EDA / accelerator cohorts (PowerUp) | 5 | 4 | 5 | 4 | 5 | 5 | **28** | **GO P0** | White-label seat + partner report | cohort, board, compliance, market |
| **S3** | Agritech / foodtech micro-ventures | 5 | 3 | 5 | 3 | 5 | 5 | **26** | **GO** | Hybrid edge bundle narrative | grants, market, finance, board |
| **S4** | Pre-Series A SaaS / fintech | 4 | 4 | 4 | 3 | 5 | 3 | **23** | **GO** | Active tier + Xero/RDTI | finance, funding, legal, board |
| **S5** | Healthtech / medtech early | 5 | 3 | 4 | 2 | 5 | 4 | **23** | **Pilot** | Privacy Act + HITL pack | compliance, legal, board |
| **S6** | Māori / iwi-linked ventures | 4 | 3 | 5 | 2 | 5 | 5 | **24** | **Pilot** | Cultural pack (HITL cultural) | compliance, formation, board |
| **S7** | Climate / cleantech grant-heavy | 4 | 3 | 4 | 3 | 4 | 4 | **22** | **GO** | Grants + RDTI dogfood | grants-rdti, funding, board |
| **S8** | Accountants / bookkeepers (channel) | 3 | 4 | 3 | 3 | 4 | 3 | **20** | **Pilot** | Handoff packs + referral | finance, invoice, handoff |
| **S9** | Mid-market enterprise (100+) | 3 | 4 | 2 | 1 | 5 | 2 | **17** | **Watch** | Not core; standards mapping only | enterprise-adoption, compliance |
| **S10** | Big-4 / large consultancies | 2 | 5 | 2 | 1 | 4 | 2 | **16** | **Watch** | Complement / white-label IP later | enterprise-adoption |
| **S11** | Telco / bank agent platforms | 2 | 3 | 1 | 1 | 3 | 1 | **11** | **No** | Adjacent only | — |
| **S12** | Local government / councils | 4 | 3 | 3 | 1 | 5 | 5 | **21** | **Pilot** | Procurement pack + Algorithm Charter | enterprise-adoption, compliance |

### Ranking for GTM (next 90 days)

1. **S2 EDA cohorts** (Venture Taranaki PowerUp) — highest total + regional proof  
2. **S1 Solo founders** — volume + dogfood  
3. **S3 Agritech** — CAT hybrid edge story + primary industries  
4. **S7 Climate / S4 SaaS** — grant and compliance pull  
5. **S6 / S12** — high impact, slower sales; cultural + procurement HITL  

---

## 2. Enterprise adoption matrix (how *enterprises* adopt — create markets)

Enterprises do not “download a founder OS” the same way. We open markets by **productising trust artefacts** they already buy (compliance, procurement answers, cohort tooling, RDTI hygiene).

| Adoption product | Enterprise buyer | Job to be done | What we ship | Revenue shape | Skill / doc |
|------------------|------------------|----------------|--------------|---------------|-------------|
| **A. EDA fleet seats** | Accelerator / EDA | Scale mentor capacity without hiring 10 ops staff | White-label pack + partner report | Per-seat 90-day pilot → annual | `cohort`, `docs/VT_POWERUP_APPROACH.md` |
| **B. RDTI evidence OS** | Founder + tax advisor | Defensible contemporaneous R&D logs | `rdti` + audit + board pack | Founder sub + advisor channel | `grants-rdti-clerk` |
| **C. Procurement trust pack** | Council / gov-adjacent / mid-market | Answer Algorithm Charter / Privacy / HITL DD | standards-mapping + compliance gate report | Paid pilot / licence | `enterprise-adoption-officer` |
| **D. Finance handoff** | SME + accountant | GST/invoice triage without agent email risk | bank/invoice/handoff zips | Founder tier + accountant referral | `finance-clerk` |
| **E. Hybrid edge story** | Agritech co-ops / farms | Local inference + founder ops in one narrative | Portfolio link + board pack | Bundle with Byte Size Kai / SoilGuard | market + portfolio matrix |
| **F. Investor readiness** | Pre-seed founder | Data room + honest market claims | seed pack + investor-readiness skill | Included in Active | `investor-readiness-clerk` |
| **G. Cultural sovereign stack** | Iwi / Māori enterprise (gated) | Data sovereignty + HITL | Te Mana Raraunga docs + cultural flags | Relationship-first; no cold sell | compliance, cultural HITL |

### Market-creation thesis (seed narrative)

> We are not only selling software seats. We are creating a **category**: *jurisdiction-native digital employees for NZ founders and the EDAs that serve them* — with hard legal ceilings, local-first data, and procurement-ready control mapping. That category does not exist as a productised installable fleet in public NZ market maps (July 2026).

---

## 3. Competitive fit (positioning)

| Competitor type | Their play | Our wedge | Avoid |
|-----------------|------------|-----------|-------|
| AgentWorks-style SME agents | Service + Xero bots | Installable fleet + RDTI + EDA white-label + HITL code | Price race on invoice bots |
| Agentic consultancies | Projects | Product + dual licence IP | Becoming pure services |
| Big-4 / Arcanum enterprise | Mid-market platforms | Pre-seed / EDA / founder beachhead first | Fake “we’re enterprise-ready for Fonterra tomorrow” |
| ChatGPT + Notion stack | Free DIY | Deterministic GST/RDTI/board + audit trail | Competing on chat quality alone |

---

## 4. Score a live prospect (operators)

```bash
nz-startup market matrix              # print full matrix
nz-startup market score --segment S2  # EDA cohort
nz-startup market score --segment S1 --json
nz-startup market enterprise          # adoption products A–G
```

Agents: use this file + `knowledge/nz-market-stats.md` before inventing TAM.

---

## 5. Seed investment attractiveness (how this matrix helps raise)

| Investor question | Matrix answer |
|-------------------|---------------|
| Who pays first? | S2 EDA (PowerUp pilot) + S1 founders |
| Why now? | $754m NZ capital 2025 but only 47 first-funded → admin efficiency is existential |
| Why defensible? | Jurisdiction depth + HITL in code + dual licence + Te Mana Raraunga |
| Path to larger markets? | A→C→E: EDA seats → procurement trust → hybrid edge agritech |
| Risks? | S9/S10 slow enterprise cycles; do not burn runway chasing 100+ headcount accounts pre-seed |

See also: [`docs/SEED_INVESTOR_PACK.md`](./SEED_INVESTOR_PACK.md) · [`docs/PORTFOLIO_MARKET_FIT.md`](./PORTFOLIO_MARKET_FIT.md)
