"""
Founder onboarding wizard — first-hour setup without send/file/pay.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from nz_startup import calendar_ops, grants, memory, pipeline, status, weekly
from nz_startup.audit import append_audit
from nz_startup.paths import company_dir


def run_onboard(
    company_id: str,
    *,
    legal_name: str = "",
    trading_name: str = "",
    region: str = "Aotearoa New Zealand",
    wedge: str = "",
    icp: str = "",
    force: bool = False,
) -> dict[str, Any]:
    """
    Initialise company memory (if needed), seed starter ops artefacts,
    write 30-day plan, weekly board, and status.
    """
    steps: list[dict[str, Any]] = []
    created = False
    try:
        path = memory.init_company(company_id, force=force)
        created = True
        steps.append({"step": "init_company", "ok": True, "path": str(path)})
    except FileExistsError:
        steps.append({"step": "init_company", "ok": True, "note": "already exists"})
        path = company_dir(company_id)

    # Profile overlay (non-secret)
    profile_path = company_dir(company_id) / "profile.md"
    if legal_name or trading_name or wedge or icp:
        profile = (
            f"# Company Profile\n\n"
            f"- Legal name (or proposed): {legal_name or 'TBD'}\n"
            f"- Trading name: {trading_name or legal_name or 'TBD'}\n"
            f"- Entity type: NZ limited company (confirm)\n"
            f"- Region: {region}\n"
            f"- NZBN: pending\n"
            f"- Wedge / ICP: {wedge or 'TBD'} / {icp or 'TBD'}\n"
            f"- Data residency: local-first default\n"
            f"- Cultural partnerships: none claimed\n"
        )
        profile_path.write_text(profile, encoding="utf-8", newline="\n")
        steps.append({"step": "profile", "ok": True})
    else:
        steps.append({"step": "profile", "ok": True, "note": "left example/default profile"})

    # Starter pipeline if empty
    if not pipeline.list_deals(company_id):
        pipeline.add_deal(
            company_id,
            account="First discovery target",
            stage="lead",
            next_step="book discovery conversation (not a pitch)",
            source="onboard",
        )
        steps.append({"step": "pipeline_seed", "ok": True})
    else:
        steps.append({"step": "pipeline_seed", "ok": True, "note": "already has deals"})

    # Calendar defaults + 30d incorporation reminder
    calendar_ops.seed_defaults(company_id)
    due = (date.today() + timedelta(days=30)).isoformat()
    calendar_ops.add_item(
        company_id,
        item="30-day onboard review — pipeline ≥ 6 conversations?",
        due=due,
        category="ops",
        notes="From onboard wizard",
    )
    steps.append({"step": "calendar", "ok": True})

    # Grants seed
    seeded = grants.seed_nz_starters(company_id)
    steps.append(
        {
            "step": "grants_seed",
            "ok": True,
            "added": len(seeded) if isinstance(seeded, list) else 0,
        }
    )

    # 30-day plan
    plan_path = _write_30_day_plan(company_id, legal_name or company_id, wedge, icp)
    steps.append({"step": "plan_30_day", "ok": True, "path": str(plan_path)})

    # Decision log
    memory.append_decision(
        company_id,
        f"Onboarded via nz-startup wizard ({date.today().isoformat()})",
    )

    weekly_path = weekly.generate_weekly_review(company_id)
    steps.append({"step": "weekly", "ok": True, "path": str(weekly_path)})

    st, status_path = status.write_status(company_id)
    steps.append(
        {"step": "status", "ok": True, "score": st.get("score"), "path": str(status_path)}
    )

    append_audit(
        company_dir(company_id),
        actor="cli:nz-startup",
        skill="nz-startup-fleet",
        action="onboard_wizard",
        summary=f"Onboarded {company_id} score={st.get('score')}",
        artefact_ref="onboard/30-day-plan.md",
        tier="gold",
    )

    return {
        "company_id": company_id,
        "created": created,
        "score": st.get("score"),
        "band": st.get("band"),
        "steps": steps,
        "paths": {
            "profile": str(profile_path),
            "plan_30_day": str(plan_path),
            "weekly": str(weekly_path),
            "status": str(status_path),
        },
        "next_human_actions": [
            "Edit profile.md with real non-secret facts",
            "Replace starter pipeline account with named targets",
            "Start RDTI log on day one of R&D: nz-startup rdti add …",
            "Charge for pilots — free pilots don't convert",
            "Run nz-startup demo run before EDA meetings",
        ],
        "hitl": "Onboarding prepares artefacts only — humans file, send, and pay.",
    }


def _write_30_day_plan(
    company_id: str, name: str, wedge: str, icp: str
) -> Path:
    company = company_dir(company_id)
    out = company / "onboard"
    out.mkdir(exist_ok=True)
    path = out / "30-day-plan.md"
    today = date.today()
    d30 = today + timedelta(days=30)
    text = f"""# 30-day founder plan — {name}

Generated: {today.isoformat()} · Review by: {d30.isoformat()}  
**DRAFT — human owns decisions**

## Wedge

- Product wedge: {wedge or '_TBD — write THE wedge down_'}
- ICP: {icp or '_TBD_'}

## Days 1–30 checklist

### Company
- [ ] Confirm name / structure; prepare incorporation pack (`formation-officer`)
- [ ] Founder files incorporation via RealMe when ready
- [ ] IRD / GST registration decision; bank account requirements list
- [ ] Start RDTI activity log contemporaneously (never invent hours)

### Pipeline (the only thing that matters)
- [ ] Map 10 named targets (not anonymous segments)
- [ ] Book 8 discovery conversations (not pitches)
- [ ] Identify 3 who would take a **paid** pilot
- [ ] Draft one-page pilot offer (see `nz-startup pilot offer`)

### Product
- [ ] One working demo asset (film it)
- [ ] Nothing new gets built that isn't required by a signed pilot

### Funding admin
- [ ] Register interest / calendar for relevant EDA programmes
- [ ] Keep grants tracker updated (`nz-startup grants rank`)

## Rules
1. Charge from day one where possible  
2. Agents draft/prepare only — you file, send, pay  
3. Weekly board every week: `nz-startup weekly {company_id}`

## Autonomy slogan
Agents inform, draft, prepare, monitor, and remind.  
Humans advise, sign, file, send, and pay.
"""
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def format_onboard_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Onboard complete — `{result.get('company_id')}`",
        "",
        f"- Created new memory: {result.get('created')}",
        f"- Status score: **{result.get('score')}/100** ({result.get('band')})",
        "",
        result.get("hitl", ""),
        "",
        "## Steps",
        "",
    ]
    for s in result.get("steps") or []:
        lines.append(f"- **{s.get('step')}** — {'OK' if s.get('ok') else 'FAIL'}")
    lines.extend(["", "## Paths", ""])
    for k, v in (result.get("paths") or {}).items():
        lines.append(f"- {k}: `{v}`")
    lines.extend(["", "## Next human actions", ""])
    for a in result.get("next_human_actions") or []:
        lines.append(f"- [ ] {a}")
    lines.append("")
    return "\n".join(lines)
