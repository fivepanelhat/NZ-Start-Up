# Contributing

## Principles

1. Preserve autonomy ceilings.  
2. Keep NZ knowledge current (stale grant info is harmful).  
3. Classify changes Gold / Diamond / Platinum.  
4. Add tests when adding skills.

## Workflow

1. Branch from `main`  
2. Edit skill + changelog  
3. `python scripts/validate_skills.py && pytest -q`  
4. PR with tier classification in description  

## Skill checklist

- [ ] Directory name matches `name`  
- [ ] `requires_hitl` and `cultural_sensitivity` set  
- [ ] Guardrails section present  
- [ ] References / templates linked  
- [ ] HITL matrix updated if autonomy changed  
