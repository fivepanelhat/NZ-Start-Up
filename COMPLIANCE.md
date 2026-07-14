# NZ Start-Up in a Box — Compliance Framework

**Coastal Alpine Tech Limited** · Aligned with Aether Compliance, Te Tiriti o Waitangi, and Te Mana Raraunga.

## Purpose

Compliance is a **design constraint**, not a post-hoc checklist. This fleet helps founders operate inside NZ law; it must never pretend to replace authorised agents, lawyers, accountants, or cultural advisors.

## 1. Te Mana Raraunga & Māori data sovereignty

Principles applied:

| Principle | Product implication |
|-----------|---------------------|
| Rangatiratanga | Founder (and iwi partners) retain authority over their data |
| Kaitiakitanga | Local-first memory; minimise exfiltration |
| Whakapapa | Company memory keeps relational context (decisions, people, whenua links) |
| Manaakitanga | Careful language; no extractive “Māori branding” |
| Kotahitanga | White-label and cohort features serve collective capacity |

Implementation: company memory defaults local; cultural_sensitivity high skills require HITL; no silent offshore export of Māori / farm / health data.

## 2. Human-in-the-loop (HITL)

| Layer | Rule |
|-------|------|
| Agents | Inform, draft, prepare, monitor, remind |
| Humans | Advise, sign, file, send, pay |

See `compliance/hitl-matrix.md` for per-employee ceilings.

## 3. NZ legal hard stops

| Regime | Product rule |
|--------|--------------|
| Lawyers and Conveyancers Act 2006 | No legal advice; drafts watermarked |
| FMC Act | No regulated financial advice; term sheets flagged for lawyer |
| Tax agent / IRD | Never file returns or move money |
| UEM Act 2007 | No autonomous unsolicited electronic messages |
| Companies Act 1993 | Prep only; founder authenticates filing |
| Privacy Act 2020 | Minimise; disclose; secure; access rights |
| Health and Safety at Work Act 2015 | Checklists only; not a PCBU risk assessment substitute |

## 4. Privacy Act 2020 (IPP summary for product design)

1. Purpose of collection disclosed  
2. Source of personal information preferred from individual  
3. Collection limited to what is needed  
4. Manner of collection lawful and fair  
5. Storage and security reasonable  
6. Access rights  
7. Correction rights  
8. Accuracy before use  
9. Retention limits  
10–13. Use, disclosure, unique identifiers controlled  

**Default architecture argument:** local-first desktop / skills pack reduces hosting of other companies’ financial and legal data (argument against premature multi-tenant SaaS).

## 5. Security

- No secrets in repository  
- Input validation on any future MCP tools  
- Audit log schema for agent actions (`compliance/audit-log-schema.md`)  
- Separation of draft artefacts vs submitted artefacts in company memory  

## 6. Cultural safety

Skills that touch iwi engagement, whenua, or Māori funding pathways declare `cultural_sensitivity: high` and require human + cultural review readiness. See Aether `te-mana-raraunga-sovereignty` patterns.

## 7. Transparency

- Skills versioned  
- Weekly operating review is the product surface of accountability  
- Claims of “SOC 2 certified” etc. are forbidden unless independently true  

## 8. Limitations

This product is **not**:

- A law firm, accounting practice, or financial advice provider  
- An authorised Companies Office agent  
- A fully autonomous workforce  
- A substitute for RealMe-authenticated government transactions  

## Ongoing commitments

- Living knowledge of NZ grant and agency landscape (content decays fast)  
- Confirm statute application with NZ counsel before commercial shipping claims  
- Evolve this document with Aether COMPLIANCE.md  

**Maintained as part of Coastal Alpine Tech / NZ Start-Up in a Box.**
