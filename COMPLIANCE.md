# COMPLIANCE.md

**Coastal Alpine Tech Limited** | **Product:** NZ Start-Up in a Box
Last updated: 19 July 2026

> Super Grok compliance briefing (19 July 2026). This is **alignment evidence**, not a compliance certificate or legal advice.

## Regulatory Mapping

### New Zealand
- Privacy Act 2020 + **IPP 3A** (Privacy Amendment Act 2025) - effective **1 May 2026**  
  Notification required when personal information is collected indirectly.
- Biometric Processing Privacy Code 2025  
  New biometric processing: 3 November 2025  
  Existing biometric processing: 3 August 2026
- Health Information Privacy Code (applies where health / wellbeing data is processed)
- Te Mana Raraunga principles - primary data sovereignty framework

### European Union
- **EU AI Act** - Annex III high-risk obligations enforceable **2 August 2026**
- Relevant high-risk categories:
  - Health decision support
  - Biometrics (remote identification, categorisation, emotion recognition)
  - Critical infrastructure / essential services
- Required: risk management, data governance, technical documentation, human oversight, logging, transparency, post-market monitoring

### International Standards
- **ISO/IEC 42001** - AI Management System (AIMS)  
  Covers AI policy, risk assessment, data governance, human oversight, monitoring, continual improvement
- **SOC 2** - Security, Availability, Confidentiality, Processing Integrity, Privacy  
  Priority for multi-tenant / customer-facing components

### Core Technical Controls (Mandatory)
- Local-first / offline-native processing by default
- Owner-controlled encryption keys
- No silent data exfiltration
- Explicit Human-in-the-Loop (HITL) gates for high-impact and culturally sensitive decisions
- Data residency under New Zealand control

### Scope Notes
- Current systems prioritise offline-native operation and data minimisation.
- Any future multi-tenant or customer-facing features will be assessed against SOC 2 and EU AI Act high-risk requirements before release.

### Limitations
- Not legal advice; not a certification claim.
- Confirm statute application with NZ counsel before commercial shipping claims.
- Agents inform / draft / prepare only; humans advise / sign / file / send / pay.

---

## Product-specific mapping

**Coastal Alpine Tech Limited - Pre-seed** | Taranaki | Aotearoa New Zealand 
**R&D since 8 August 2025** | **Founded 8 August 2026** 
Aligned with Aether compliance patterns, Te Tiriti o Waitangi principles, and Te Mana Raraunga.

**Licence:** Dual (proprietary Track A + commercial Track B) - see `LICENSE`, `LICENSE-COMMERCIAL.md`, `docs/DUAL_LICENCE.md`. **Not open source.** Protected under the **Copyright Act 1994 (NZ)**.

## Purpose

Compliance is a **design constraint and runtime gate**, not a post-hoc checklist. This fleet helps founders operate inside NZ law; it must never replace authorised agents, lawyers, accountants, or cultural advisors.

Runtime entry points: `nz-startup compliance check` | `nz-startup harden status` | skill `agent-hardening` | `compliance/*`.

---

## 0. Compliance control plane (hardened)

| Control | Location | Enforcement |
|---------|----------|-------------|
| Autonomy ceiling | `hitl.py`, `agent_guardrails.py` | Block send/file/pay/sign tools and phrases |
| Secret refusal | `agent_guardrails.scan_secrets` | Refuse PEM/API-key shaped writes |
| Path sandbox | `resolve_sandboxed_path` | Company memory only |
| Watermarks | `WATERMARKS` | Draft / not advice / not sent labels |
| HITL matrix | `compliance/hitl-matrix.md` | Per-employee ceilings |
| Legal hard stops | `compliance/legal-boundaries-nz.md` | Act-level boundaries |
| Privacy | `compliance/privacy-act-2020.md` | IPP product checklist |
| Te Mana Raraunga | `compliance/te-mana-raraunga.md` | Cultural/data sovereignty |
| Audit | `compliance/audit-log-schema.md` | JSONL agent actions |
| Gate report | `nz-startup compliance check` | Machine-readable pass/fail |
| Licence | `LICENSE` + `LICENSE-COMMERCIAL.md` | Dual proprietary/commercial; NZ copyright |
| Pre-seed identity | `ABOUT.md` | CAT dates, Taranaki, founding context |

**Gate rule:** Production use of the product under a commercial licence still requires human responsibility for regulated outcomes. Software gates reduce risk; they do not create a compliance certificate.

---

## 1. Te Mana Raraunga & Maori data sovereignty

| Principle | Product implication |
|-----------|---------------------|
| Rangatiratanga | Founder (and iwi partners) retain authority over their data |
| Kaitiakitanga | Local-first memory; minimise exfiltration |
| Whakapapa | Company memory keeps relational context |
| Manaakitanga | Careful language; no extractive "Maori branding" |
| Kotahitanga | White-label and cohort features serve capacity, not extraction |

**Hard rules**

- Do not invent iwi endorsement or partnership 
- `cultural_sensitivity: high` skills require human + cultural review readiness 
- Reject silent offshore export of Maori / whenua-linked / health data designs 
- No "Maori framing" for grant fit without a stated relationship pathway 

---

## 2. Human-in-the-loop (HITL)

| Layer | Rule |
|-------|------|
| Agents | Inform, draft, prepare, monitor, remind |
| Humans | Advise, sign, file, send, pay |

See `compliance/hitl-matrix.md`. Runtime forbids tools/actions that cross the line.

---

## 3. NZ legal hard stops

| Regime | Product rule |
|--------|--------------|
| Lawyers and Conveyancers Act 2006 | No legal advice; drafts watermarked |
| FMC Act | No regulated financial advice |
| Tax agent / IRD | Never file returns or move money |
| UEM Act 2007 | No autonomous unsolicited electronic messages |
| Companies Act 1993 | Prep only; founder authenticates filing |
| Privacy Act 2020 | Minimise; secure; access/correction |
| Health and Safety at Work Act 2015 | Checklists only - not PCBU substitute |
| Human Rights Act | Hiring later-hire skill must not encode unlawful discrimination |

Confirm statute application with NZ counsel before commercial shipping claims.

---

## 4. Privacy Act 2020 (product design)

Default: **local company memory**, no secrets in git, draft vs submitted separation, audit log.

IPP-oriented checklist: purpose, minimisation, security, access, correction, retention, overseas disclosure control - see `compliance/privacy-act-2020.md`.

**Hosting argument:** multi-tenant SaaS that holds others' financial/legal data is deferred until funded compliance programme exists.

---

## 5. Security & proprietary protection

- No secrets in repository 
- Input validation / path sandbox on tools 
- Audit schema for agent actions 
- Proprietary licence - no redistribution without commercial agreement 
- Console binds localhost only 

See `SECURITY.md` and `LICENSE`.

---

## 6. Cultural safety

Skills touching iwi engagement, whenua, or Maori funding declare high cultural sensitivity and require review pathways. See Aether `te-mana-raraunga-sovereignty` patterns and `compliance/te-mana-raraunga.md`.

---

## 7. Transparency & auditability

- Skills versioned 
- Weekly operating review as accountability surface 
- Claims of "SOC 2 certified" etc. forbidden unless independently true 
- `audit.jsonl` for material agent actions 

---

## 8. Regulated output watermarks (mandatory)

| Domain | Watermark |
|--------|-----------|
| Any agent draft | PREPARED BY AGENT - human must verify |
| Legal | NOT LEGAL ADVICE |
| Finance / investment | NOT FINANCIAL ADVICE |
| Outreach | DRAFT_NOT_SENT (UEM Act) |
| Compliance checklist | INFORMATION ONLY - not a compliance certificate |
| Filings | DRAFT - NOT FOR SUBMISSION |

---

## 9. Compliance gate (runtime)

```bash
nz-startup compliance check
nz-startup compliance check --company my-startup
nz-startup compliance report --json
```

Checks (examples):

1. Proprietary LICENSE present (not Apache) 
2. HITL matrix + legal boundaries files present 
3. Hardening skill + guardrails module present 
4. Forbidden MCP tools absent from inventory 
5. Optional company: audit log exists; no obvious secret files in tree 

---

## 10. Limitations

This product is **not**:

- A law firm, accounting practice, or financial advice provider 
- An authorised Companies Office agent or tax agent 
- A fully autonomous workforce 
- Open-source software (proprietary licence) 
- A substitute for RealMe-authenticated government transactions 

---

## Ongoing commitments

- Living NZ grant/agency knowledge (content decays) 
- Evolve with Aether compliance patterns 
- Commercial licencees remain controllers of their founder data 

**Maintained by Coastal Alpine Tech Limited.**
