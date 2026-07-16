# Dual licence (pre-seed) - protecting IP under New Zealand copyright law

**Coastal Alpine Tech Limited - Pre-seed** 
**Product:** NZ Start-Up in a Box 
**Not legal advice.** Confirm commercial terms with an NZ lawyer before signing customers.

---

## What "dual licence" means here

This product is **not open source**. Dual licensing is used as a **commercial IP strategy**:

| Track | Instrument | Who it is for |
|-------|------------|---------------|
| **A - Default / evaluation** | Proprietary Software Licence (`LICENSE`) | Public evaluation of the repo; no production rights |
| **B - Commercial** | Commercial / white-label / cohort licence (`LICENSE-COMMERCIAL.md` terms) | Paying founders, EDAs, accelerators, OEM partners |

Both tracks sit on top of **automatic copyright** under New Zealand law. Dual licence does **not** put the code under MIT/Apache. It means:

1. **Copyright is reserved** by Coastal Alpine Tech Limited. 
2. **Track A** is the default: limited evaluation, no redistribution. 
3. **Track B** is granted only by written agreement (or paid subscription terms) and can include production use, white-label, and cohort seats.

```text
 NZ Copyright Act 1994
 (automatic protection)
 |
 ------------------------------
 
 Track A - Proprietary Track B - Commercial
 LICENSE (default) LICENSE-COMMERCIAL.md
 view / evaluate only production | white-label
 | cohort / OEM by agreement
```

---

## Why this helps at pre-seed

| Goal | How dual + copyright helps |
|------|----------------------------|
| Stop free resale of skills pack | Proprietary default; no OSS grant |
| Sell white-label to EDAs | Commercial track with seat/cohort terms |
| Keep R&D value | Copyright protects source, docs, skills, templates as literary works |
| Clear investor story | "IP owned by CAT; licensed commercially" |
| Still show the work | Public repo for credibility without giving away ownership |

---

## New Zealand copyright (plain English)

Under the **Copyright Act 1994 (NZ)**:

- Original software, documentation, and creative works are generally **protected automatically** when created - you do **not** need to register copyright in NZ for protection to exist. 
- Copyright is a **property right** in the work (code, skills markdown, architecture docs, distinctive templates). 
- **Copyright notice** (`Copyright year owner`) is good practice and appears in `LICENSE`, `NOTICE`, and source headers. 
- **Licence** is how you grant (or refuse) others permission to use the work. Dual licence = two permission tracks, same owner. 
- **Trade secrets / confidential information** (e.g. unpublished commercial terms, private keys, customer data) are protected separately - keep them out of git. 
- **Trade marks** (name/logo) are separate from copyright; consider registration for "Coastal Alpine Tech" / product marks as the brand grows. 
- **Patents** are optional and rare for pure software stacks; do not assume patents exist.

This product also respects **third-party licences** for dependencies (e.g. optional `mcp`, `pypdf`, `pywebview`) and Aether patterns under *their* licences - dual licence here does **not** re-license those components.

---

## Pre-seed operating rules

1. **Default assumption:** anyone without a commercial agreement is on Track A only. 
2. **Production use** by customers or EDA cohorts requires Track B (written or paid terms). 
3. **Do not** remove copyright or proprietary notices. 
4. **Do not** publish private customer memory, IRD numbers, or bank data. 
5. **RDTI / R&D narrative:** contemporaneous logs support *your* R&D claims; licence track is separate from RDTI eligibility. 
6. **Cultural IP:** Te Mana Raraunga / whenua-linked knowledge is not free-for-all marketing content; human and cultural review still apply.

---

## Timeline (Coastal Alpine Tech)

| Milestone | Date |
|-----------|------|
| Research & development commenced | **8 August 2025** |
| Company founding / incorporation target | **8 August 2026** |
| Product stage | **Pre-seed** |

---

## Founding context (Taranaki)

Coastal Alpine Tech is a **Taranaki, Aotearoa New Zealand** pre-seed venture. Founding context includes **Wayne Roberts** and **Taranaki whanau** with **six generations in agriculture** on whenua in Taranaki - grounding sovereign AI and agritech work in long-run care for land and community, not extractive branding.

Maori development framing in this repo must follow Te Mana Raraunga principles: no invented iwi endorsement, no cultural extraction, HITL for culturally sensitive outputs.

---

## Files

| File | Role |
|------|------|
| `LICENSE` | Track A - Proprietary (default) |
| `LICENSE-COMMERCIAL.md` | Track B - commercial / white-label terms (outline) |
| `NOTICE` | Copyright + dual-track notice |
| `compliance/proprietary-licence.md` | Ops summary |
| `docs/DUAL_LICENCE.md` | This explanation |

---

## Disclaimer

This document is **information for product design and pre-seed IP hygiene**. It is **not legal advice**. Have an NZ lawyer review dual-licence wording before issuing paid licences or raising capital on IP claims.
