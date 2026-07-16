# Optimization execution log — Claude reports #6–11

**Date:** 2026-07-16  
**Grounding:** Claude gap analysis (G1–G15), final review T1–T9, adoption report #10, collab map #11, investor one-liner #9.  
**Rule:** Do not break e2e. Prefer evidence over new structure.

---

## Already closed in-repo (do not rebuild)

| Claude item | Evidence |
|-------------|----------|
| G1 / T1 evals | `nz-startup eval` + `--live` lane |
| G2 / T2 quarantine | `untrusted.py` + injection tests |
| G3 allow-list HITL | `hitl.py` default-deny |
| G4 freshness | knowledge frontmatter + CI discipline |
| G5 lockfile + pip-audit | `requirements-lock.txt`, strict audit |
| G6 / T5 scheduler | `schedule install` → Windows task present |
| G7 tasks | `tasks` CLI |
| G8 telemetry | `audit export` OTel-shaped |
| G9 routing/budgets | `budget` CLI |
| G10 INDEX/compaction | `index` CLI |
| G11 console token | `console` session token |
| G12 policy vs branding | ABOUT / README vs pure policy modules |
| G13 MCP | single `mcp.json` pattern |
| G14 pack | `pack` zip + SHA256 + SBOM |
| T4–T9 trust layer | See Claude final review #8 |

---

## Executed this session (2026-07-16)

| Action | Result | Break risk |
|--------|--------|------------|
| `doctor` | PASS | Low |
| `smoke` | PASS | Low |
| `compliance check` | PASS | Low |
| `pytest` | 100 passed (pre-change baseline) | Low |
| Dogfood onboard `coastal-alpine-tech` | Local memory + RDTI + VT pipeline lead | **Local only** (gitignored) |
| `schedule install` + `schedule run` | Task `NZ-Startup-WeeklyCadence`; heartbeat OK | OS task (uninstall: `schedule uninstall`) |
| `backup create` | Fernet path, manifest with `encryption_path` | Local passphrase never committed |
| `eval --live --write` | 3/3 pass; provider=`rubric` (honest) | Low |
| `demo run` for VT | status 100; board pack zip | Low |
| Docs: REALITY, EDA kit, legal checklist, this log | Added | Low |
| Blue-Moon claim hygiene | Separate PR | Low |

---

## Explicitly NOT done (grounded)

| Item | Why |
|------|-----|
| Email Venture Taranaki | **UEM Act / HITL** — human must personalise and send |
| Claim partnership with VT / Kotahitanga / startups.com | No signed deals |
| LLM-as-judge eval with live API | No model keys configured; rubric is correct fallback |
| Commit company memory | Gitignored by design (founder data residency) |
| Lawyer review of dual licence | Human booking required — checklist prepared only |

---

## Verification commands (reproduce)

```bash
cd NZ-Start-Up
python -m pip install -e ".[dev]"
python -m pytest -q
python -m nz_startup doctor
python -m nz_startup smoke
python -m nz_startup compliance check
python -m nz_startup schedule verify
python -m nz_startup eval --live --json
python -m nz_startup demo run --company demo-vt --partner "Venture Taranaki" --programme "PowerUp demo"
```

---

## Next human actions (binding constraint = business clock)

1. Personalise and **send** `docs/VT_POWERUP_APPROACH.md` outreach (or decide not to).  
2. Run CAT on the fleet daily so dogfood memory accumulates.  
3. Cold-start: install pack zip on a clean Windows machine (film it).  
4. One hour NZ startup lawyer on dual licence + standards-mapping language.  
5. One wedge pilot evidence (Byte Size Kai field **or** FLW live product) before quoting higher valuation bands.
