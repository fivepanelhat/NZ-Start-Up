"""
First-principles operator / digital employee brief.

Produces a ruthless priority board for the founder — high agency preparation,
zero autonomous filing/sending/payment. Inspired by first-principles operating
cadence (physics of the company: cash, time, learning rate, revenue path).
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from nz_startup import calendar_ops, grants, pipeline, rdti, status, tasks
from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists, read_file
from nz_startup.paths import company_dir

# Physics of a pre-seed company (ordered by constraint severity)
PHYSICS = (
    ("cash_runway", "Cash / runway — without oxygen nothing else matters"),
    ("revenue_path", "Revenue path — who pays, when, and for what"),
    ("learning_rate", "Learning rate — RDTI / experiments that de-risk the wedge"),
    ("compliance_time", "Compliance clocks — fines and dead companies from missed filings"),
    ("distribution", "Distribution — pipeline motion and paid pilot next steps"),
    ("product_reality", "Product reality — ship evidence, not deck fiction"),
)


def _safe_read(company_id: str, rel: str, limit: int = 800) -> str:
    try:
        return read_file(company_id, rel)[:limit]
    except FileNotFoundError:
        return f"_Missing {rel}_"


def _top_tasks(company_id: str, n: int = 8) -> list[dict[str, Any]]:
    rows = tasks.list_tasks(company_id)
    open_rows = [r for r in rows if r.get("status") in ("todo", "in_progress", "blocked")]
    # prefer blocked then in_progress then todo; due-date first
    def key(r: dict[str, Any]) -> tuple:
        st = {"blocked": 0, "in_progress": 1, "todo": 2}.get(r.get("status", "todo"), 9)
        due = r.get("due") or "9999-99-99"
        return (st, due)

    open_rows.sort(key=key)
    return open_rows[:n]


def _pipeline_pressure(company_id: str) -> dict[str, Any]:
    deals = pipeline.list_deals(company_id)
    active = [d for d in deals if d.get("stage") not in ("won", "lost", "")]
    stalled = [
        d
        for d in active
        if not (d.get("next_step") or "").strip()
        or (d.get("stage") or "") in ("lead", "discovery")
    ]
    return {
        "total": len(deals),
        "active": len(active),
        "stalled_or_early": len(stalled),
        "sample": active[:5],
    }


def _calendar_pressure(company_id: str) -> dict[str, Any]:
    try:
        rem = calendar_ops.reminders(company_id, within_days=14)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e), "overdue": [], "actionable": 0}
    return {
        "actionable": rem.get("count_actionable", 0),
        "overdue": rem.get("overdue") or [],
        "upcoming": (rem.get("upcoming") or [])[:8],
    }


def collect_operator_state(company_id: str) -> dict[str, Any]:
    """Aggregate company physics for the digital employee brief."""
    ensure_exists(company_id)
    st = status.collect_status(company_id)
    pipe = _pipeline_pressure(company_id)
    cal = _calendar_pressure(company_id)
    rdti_rows = rdti.list_entries(company_id, limit=20)
    grant_rows = grants.list_grants(company_id)
    open_tasks = _top_tasks(company_id)
    profile = _safe_read(company_id, "profile.md", 600)
    runway = _safe_read(company_id, "runway.md", 600)

    # Priority engine (first principles, not vibes)
    priorities: list[dict[str, str]] = []

    if cal.get("overdue"):
        priorities.append(
            {
                "rank": "P0",
                "physics": "compliance_time",
                "title": f"Clear {len(cal['overdue'])} overdue calendar item(s)",
                "why": "Missed compliance is company-ending; fix clocks before new features.",
                "do": "Open calendar reminders; prepare filings/drafts; human files.",
                "skill": "compliance-registrar",
            }
        )

    if pipe["active"] == 0:
        priorities.append(
            {
                "rank": "P0",
                "physics": "revenue_path",
                "title": "Zero active pipeline — invent no traction, start real motion",
                "why": "No deals = no feedback loop. Pre-seed dies on isolation.",
                "do": "Add 3 named accounts with next steps; draft outreach (never send).",
                "skill": "gtm-pipeline-rep",
            }
        )
    elif pipe["stalled_or_early"] >= max(1, pipe["active"] // 2):
        priorities.append(
            {
                "rank": "P0",
                "physics": "distribution",
                "title": "Advance stalled / early-stage deals",
                "why": "Pipeline without next steps is a spreadsheet fantasy.",
                "do": "Update next_step on every active deal; prepare paid pilot offer packs.",
                "skill": "gtm-pipeline-rep",
            }
        )

    if len(rdti_rows) == 0:
        priorities.append(
            {
                "rank": "P1",
                "physics": "learning_rate",
                "title": "Start contemporaneous RDTI / experiment log",
                "why": "Learning rate compounds; invented hours destroy claims.",
                "do": "nz-startup rdti add … with real hours, uncertainty, evidence.",
                "skill": "grants-rdti-clerk",
            }
        )

    score = st.get("score") or st.get("readiness_score") or 0
    if isinstance(score, (int, float)) and score < 50:
        priorities.append(
            {
                "rank": "P1",
                "physics": "product_reality",
                "title": f"Readiness score {score} — close memory gaps",
                "why": "Low readiness = missing profile, finance, or compliance artefacts.",
                "do": "nz-startup status; fill red gaps before investor theatre.",
                "skill": "board-chief-of-staff",
            }
        )

    if "Missing runway.md" in runway or runway.startswith("_Missing"):
        priorities.append(
            {
                "rank": "P1",
                "physics": "cash_runway",
                "title": "Write runway truth (months of oxygen)",
                "why": "Without explicit runway you cannot prioritise.",
                "do": "Edit runway.md with cash, burn, months remaining (facts only).",
                "skill": "finance-clerk",
            }
        )

    if not any(p["physics"] == "revenue_path" for p in priorities) and pipe["active"] > 0:
        priorities.append(
            {
                "rank": "P2",
                "physics": "revenue_path",
                "title": "Convert one conversation into a paid pilot next step",
                "why": "Paid pilots beat vanity demos.",
                "do": "nz-startup pilot … draft offer; human sends.",
                "skill": "gtm-pipeline-rep",
            }
        )

    if not priorities:
        priorities.append(
            {
                "rank": "P2",
                "physics": "learning_rate",
                "title": "Compound: weekly review + one hard experiment",
                "why": "When basics are green, increase rate of truth-seeking.",
                "do": "nz-startup weekly; log RDTI; ship one evidence artefact.",
                "skill": "board-chief-of-staff",
            }
        )

    # Cap to top 5
    priorities = priorities[:5]

    return {
        "company_id": company_id,
        "date": date.today().isoformat(),
        "status": st,
        "pipeline": pipe,
        "calendar": cal,
        "rdti_count": len(rdti_rows),
        "grants_count": len(grant_rows),
        "tasks": open_tasks,
        "profile_snippet": profile,
        "runway_snippet": runway,
        "priorities": priorities,
        "physics": [{"id": a, "label": b} for a, b in PHYSICS],
        "hitl": "Agents inform / draft / prepare / monitor / remind. Humans advise / sign / file / send / pay.",
    }


def format_operator_brief_markdown(state: dict[str, Any]) -> str:
    cid = state["company_id"]
    d = state["date"]
    st = state.get("status") or {}
    score = st.get("score", st.get("readiness_score", "?"))
    lines = [
        f"# Operator brief — {cid}",
        "",
        f"**Date:** {d}  ",
        f"**Mode:** Digital employee (first-principles)  ",
        f"**Readiness:** {score}  ",
        "",
        "> High agency = prepare everything. High integrity = never fake send/file/pay.",
        "",
        "## Company physics (constraints)",
        "",
    ]
    for item in state.get("physics") or []:
        lines.append(f"- **{item['id']}** — {item['label']}")

    lines += ["", "## Top priorities (do in order)", ""]
    for i, p in enumerate(state.get("priorities") or [], 1):
        lines += [
            f"### {i}. [{p['rank']}] {p['title']}",
            f"- **Physics:** `{p['physics']}`",
            f"- **Why:** {p['why']}",
            f"- **Do:** {p['do']}",
            f"- **Route skill:** `{p['skill']}`",
            "",
        ]

    pipe = state.get("pipeline") or {}
    lines += [
        "## Distribution pulse",
        "",
        f"- Deals total: **{pipe.get('total', 0)}** | active: **{pipe.get('active', 0)}** | early/stalled: **{pipe.get('stalled_or_early', 0)}**",
        "",
    ]
    for drow in pipe.get("sample") or []:
        lines.append(
            f"- `{drow.get('id', '?')}` **{drow.get('account', '?')}** "
            f"— stage `{drow.get('stage', '?')}` — next: {drow.get('next_step') or '_none_'}"
        )

    cal = state.get("calendar") or {}
    lines += [
        "",
        "## Time bombs (14-day calendar)",
        "",
        f"- Actionable: **{cal.get('actionable', 0)}** | Overdue: **{len(cal.get('overdue') or [])}**",
        "",
    ]
    for item in (cal.get("overdue") or [])[:5]:
        if isinstance(item, dict):
            lines.append(f"- OVERDUE: {item.get('item') or item}")
        else:
            lines.append(f"- OVERDUE: {item}")

    lines += [
        "",
        "## Learning rate",
        "",
        f"- RDTI log rows (recent window): **{state.get('rdti_count', 0)}**",
        f"- Grants tracked: **{state.get('grants_count', 0)}**",
        "",
        "## Open tasks",
        "",
    ]
    trows = state.get("tasks") or []
    if not trows:
        lines.append("_No open tasks in tasks.jsonl — seed with `nz-startup tasks add`._")
    for t in trows:
        lines.append(
            f"- [{t.get('status')}] `{t.get('id')}` {t.get('title')} "
            f"(skill: {t.get('skill')}, due: {t.get('due') or '—'})"
        )

    lines += [
        "",
        "## Runway snapshot",
        "",
        "```markdown",
        str(state.get("runway_snippet") or ""),
        "```",
        "",
        "## Profile snapshot",
        "",
        "```markdown",
        str(state.get("profile_snippet") or ""),
        "```",
        "",
        "## Employee standing orders",
        "",
        "1. Attack **P0** before feature cosplay.",
        "2. Every deal has a **next step** with a human owner.",
        "3. Log real R&D hours only — uncertainty + evidence required.",
        "4. Draft outreach / pilots / board packs — **human sends**.",
        "5. Prefer paid pilots and EDA white-label over free forever demos.",
        "6. Never invent NZBN, partner consent, revenue, or iwi endorsement.",
        "",
        f"**HITL:** {state.get('hitl')}",
        "",
        "## Suggested CLI cadence",
        "",
        "```bash",
        f"nz-startup operate {cid}",
        f"nz-startup status {cid}",
        f"nz-startup pipeline summary {cid}",
        f"nz-startup calendar remind {cid} --days 14",
        f"nz-startup weekly {cid}",
        f"nz-startup board pack {cid}",
        f"nz-startup console --port 8765",
        "```",
        "",
    ]
    return "\n".join(lines)


def write_operator_brief(company_id: str) -> tuple[Path, dict[str, Any]]:
    """Write operator brief to company memory and return path + state."""
    state = collect_operator_state(company_id)
    md = format_operator_brief_markdown(state)
    company = ensure_exists(company_id)
    day = state["date"]
    dest = company / "operator" / f"brief-{day}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(md, encoding="utf-8")
    latest = company / "operator" / "brief-latest.md"
    latest.write_text(md, encoding="utf-8")
    append_audit(
        company,
        actor="agent:first-principles-operator",
        skill="first-principles-operator",
        action="generate_report",
        summary=f"operator brief {day}",
        artefact_ref=str(dest.relative_to(company)),
        model_tier="standard",
        tokens_in=0,
        tokens_out=0,
        outcome="ok",
    )
    return dest, state
