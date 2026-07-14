# Security Policy

## Reporting

Email security concerns to the maintainer via GitHub Security Advisories on this repository. Do not open public issues for secrets or vulnerabilities that could expose founder data.

## Licence

This product is **proprietary** software of Coastal Alpine Tech Limited.
Unauthorised redistribution or competitive multi-tenant hosting is prohibited.
See `LICENSE`.

## Scope

NZ Start-Up in a Box is a **local-first proprietary skills pack**. Default posture:

- Founder company data stays on the founder's machine (company memory under `memory/`).
- Skills **draft and prepare**; they do not file, sign, send, or pay.
- No secrets in git (API keys, IRD numbers, bank details, RealMe credentials).
- Prefer offline / sovereign inference (Ollama / Aether) for low-stakes tasks.

## Hard boundaries (product security = legal safety)

Agents MUST NOT:

1. File with Companies Office or IRD on the founder's behalf.
2. Send unsolicited electronic messages (UEM Act 2007 risk).
3. Move money or act as a tax agent.
4. Present drafts as legal or financial advice.
5. Store or commit tax file numbers, bank credentials, or service-role keys.

## HITL

High-impact actions require human approval. See `compliance/hitl-matrix.md`.

## Disclosure timeline

We aim to acknowledge reports within 7 days and remediate critical issues in the next patch release.
