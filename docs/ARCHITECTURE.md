# Architecture

## Shape (v0.1)

```text
                    ┌─────────────────────────────┐
                    │  Board / Chief-of-Staff     │
                    │  (orchestrator skill)       │
                    └─────────────┬───────────────┘
                                  │ routes + weekly review
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   Formation … Legal        Company Memory          HITL / Audit
   (specialist skills)      (local JSON/MD)         (compliance/)
          │                       │                       │
          └───────────────────────┴───────────────────────┘
                                  │
                     CAT Standards + Aether Guardrails
```

## Design choices

| Decision | Choice | Why |
|----------|--------|-----|
| Delivery v1 | Skills pack | Fastest validation, near-zero infra (fleet design Option A) |
| Orchestration | Small orchestrator + specialists | Multi-agent fleets multiply cost/failure |
| Autonomy | Drafts-and-prepares | Legal ceilings; Gold/Platinum HITL |
| Memory | Local company memory | Privacy Act + Te Mana Raraunga default |
| NZ moat | Knowledge + templates | Jurisdiction depth, not agent tech |
| Standards | CAT Gold/Diamond/Platinum | Align with Coastal Alpine / Aether portfolio |

## Data flow (Gold unbroken chain)

```text
Formation pack → company profile
       → compliance calendar
       → RDTI activity log (from commits/timesheets)
       → market thesis
       → pipeline CRM drafts
       → content calendar
       → finance runway
       → funding / investor room
       → legal draft registry
       → weekly board report
```

Every specialist **reads and writes company memory** with clear ownership fields.

## Runtime options

1. **Aether CLI / orchestrator** — load `skills/`  
2. **Claude Code / Cowork** — install skills as plugin packs  
3. **Future desktop** — Tauri/Electron + SQLite memory + scheduled agents  
4. **Future SaaS** — multi-tenant only with funded compliance programme  

## Security model

- Tools that write files or call external APIs must pass guardrails  
- Always-require-approval actions: send email, file government forms, pay, git push of secrets  
- Audit events: `actor`, `skill`, `action`, `hitl_required`, `hitl_status`, `timestamp`, `artefact_ref`

## Relationship to Aether

This repo is a **vertical skills fleet** that depends on Aether patterns (skill format, HITL, Te Mana Raraunga, guardrails). It does not fork Aether; it consumes and extends the skill layer.
