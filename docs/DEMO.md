# EDA demo walkthrough (v0.7)

## One command

```bash
nz-startup demo run --company demo-eda --partner "Venture Taranaki" --programme "PowerUp demo"
```

Windows helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\demo_eda.ps1
```

Quick mode (pipeline + calendar + weekly only):

```bash
nz-startup demo run --company demo-eda --quick
```

## Full mode steps

1. Init company memory  
2. Seed pipeline deal for partner  
3. Calendar demo follow-up  
4. Grants seed  
5. Xero offline snapshot  
6. Bank sample import  
7. GST working papers  
8. Invoice triage sample  
9. Accountant handoff zip  
10. Weekly board  

## Artefacts

- `memory/companies/<id>/demo/demo-report-latest.md` — shareable script notes  
- Weekly board under `weekly/`  
- Handoff zip under `handoff/` (full mode)  
- Mentor board pack: `nz-startup board pack <id>` → `board-packs/board-pack-latest.zip`  
- Readiness: `nz-startup status <id>`  

## Room talking points

1. NZ jurisdiction depth is the moat  
2. Autonomy ceiling is the product  
3. Weekly board is the experience  
4. White-label seats for EDAs without SaaS risk yet  
5. Finance ends in accountant handoff — not tax-agent automation  

## Safety

Demo **never** sends email, files IRD/Companies Office, or moves money.
