# Use NZ Start-Up as your digital employee

**Product:** NZ Start-Up in a Box  
**Mode:** High-agency operator (first principles) under hard HITL ceilings  
**Not:** Fully autonomous "AI CEO" — that is illegal/unsafe for NZ tax, UEM, and Companies Office actions

---

## 1. Download

```powershell
# Windows
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

```bash
# macOS / Linux
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
chmod +x install.sh && ./install.sh
```

Manual:

```bash
python -m pip install -e ".[all]"
nz-startup install-skills
nz-startup doctor
```

---

## 2. Create *your* company memory (the employee's brain)

```bash
nz-startup onboard my-company \
  --legal-name "Your Company Limited" \
  --wedge "One sentence wedge" \
  --icp "Who pays"

# Edit real non-secret facts
# memory/companies/my-company/profile.md
# memory/companies/my-company/runway.md
```

Without profile + runway + pipeline, the employee has no physics to optimise.

---

## 3. Run the employee (daily)

```bash
# First-principles operator brief (P0 stack)
nz-startup operate my-company
# alias:
nz-startup employee my-company

# Instruments
nz-startup status my-company
nz-startup pipeline summary my-company
nz-startup calendar remind my-company --days 14

# Local dashboard
nz-startup console --port 8765
```

Brief is written to:

`memory/companies/my-company/operator/brief-latest.md`

---

## 4. What "Elon-level" means here (productised)

| Musk-style trait | How NZ Start-Up implements it |
|------------------|-------------------------------|
| First principles | Company **physics**: cash, revenue path, learning rate, compliance clocks, distribution, product reality |
| High agency | Generates ranked **P0–P2** work and drafts packs — you still decide |
| Delete lag | Stalled pipeline + overdue calendar surface first |
| Rate of learning | RDTI log requires **hours + uncertainty + evidence** |
| Multi-domain fleet | 15 skills: formation → GTM → finance → legal → board CoS |
| No bullshit metrics | Readiness score from real local artefacts, not invented ARR |
| Hard safety | HITL: inform/draft/prepare/monitor/remind only |

**It will not** send email, file Companies Office / IRD forms, move money, or invent traction. That is intentional — and what keeps you out of trouble.

---

## 5. Wire it into your AI host (so chat becomes the employee)

### Option A — Aether

```bash
nz-startup install-skills
# skills land in ~/.aether/skills (or $AETHER_SKILLS_PATH)
```

Load skill `first-principles-operator` + `board-chief-of-staff` as the front door.

### Option B — Claude Code / Cursor / Grok Build

Point the agent skills root at:

- `./skills` in this repo, or  
- the installed Aether skills path  

System instruction:

> You are the NZ Start-Up first-principles operator. Run `nz-startup operate <company>` mentally from memory files. Prefer P0 physics. Never send/file/pay. FACT / INFERENCE / UNKNOWN on claims.

### Option C — MCP

```bash
pip install -e ".[mcp]"
nz-startup mcp
```

Register `mcp.json` with your host. See `docs/MCP.md`.

---

## 6. Suggested weekly cadence

| When | Command / action |
|------|------------------|
| Mon AM | `nz-startup operate` — set P0 |
| Daily | Update pipeline next steps; log RDTI if R&D happened |
| Wed | Draft outreach / pilot packs (human sends) |
| Fri | `nz-startup weekly` + `nz-startup board pack` |
| Monthly | `nz-startup gst prepare` / grants rank / investor checklist |

---

## 7. Fleet roster (your specialist employees)

See `docs/FLEET.md`. Entry skills:

- **first-principles-operator** — priority physics (this guide)
- **board-chief-of-staff** — weekly review orchestration
- **gtm-pipeline-rep** — pipeline (never cold-blasts)
- **grants-rdti-clerk** — RDTI / grants evidence
- **finance-clerk** — runway / bank / GST papers
- **formation-officer** / **compliance-registrar** — NZ company clocks

---

## 8. Autonomy slogan (tattoo it)

> Agents inform, draft, prepare, monitor, and remind.  
> Humans advise, sign, file, send, and pay.

---

## 9. Licence

Proprietary dual licence (Track A personal/founder use defaults; commercial / white-label Track B). See `docs/DUAL_LICENCE.md`.
