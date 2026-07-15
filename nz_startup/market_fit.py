"""Market-fit matrix scoring (enterprise + segment) — deterministic, no LLM."""
from __future__ import annotations

from typing import Any

# Dimension scores 0–5; total max 30
SEGMENTS: dict[str, dict[str, Any]] = {
    "S1": {
        "name": "Solo / 1–3 person tech founders",
        "scores": {"problem": 5, "wtp": 3, "fit": 5, "speed": 5, "trust": 4, "nz_impact": 4},
        "decision": "GO",
        "entry": "Direct install + freemium",
        "skills": ["formation-officer", "finance-clerk", "grants-rdti-clerk", "board-chief-of-staff"],
    },
    "S2": {
        "name": "EDA / accelerator cohorts (PowerUp)",
        "scores": {"problem": 5, "wtp": 4, "fit": 5, "speed": 4, "trust": 5, "nz_impact": 5},
        "decision": "GO P0",
        "entry": "White-label seat + partner report",
        "skills": ["nz-startup-fleet", "board-chief-of-staff", "compliance-registrar", "market-validator"],
    },
    "S3": {
        "name": "Agritech / foodtech micro-ventures",
        "scores": {"problem": 5, "wtp": 3, "fit": 5, "speed": 3, "trust": 5, "nz_impact": 5},
        "decision": "GO",
        "entry": "Hybrid edge bundle narrative",
        "skills": ["grants-rdti-clerk", "market-validator", "finance-clerk", "board-chief-of-staff"],
    },
    "S4": {
        "name": "Pre-Series A SaaS / fintech",
        "scores": {"problem": 4, "wtp": 4, "fit": 4, "speed": 3, "trust": 5, "nz_impact": 3},
        "decision": "GO",
        "entry": "Active tier + Xero/RDTI",
        "skills": ["finance-clerk", "funding-analyst", "legal-document-assistant", "board-chief-of-staff"],
    },
    "S5": {
        "name": "Healthtech / medtech early",
        "scores": {"problem": 5, "wtp": 3, "fit": 4, "speed": 2, "trust": 5, "nz_impact": 4},
        "decision": "Pilot",
        "entry": "Privacy Act + HITL pack",
        "skills": ["compliance-registrar", "legal-document-assistant", "board-chief-of-staff"],
    },
    "S6": {
        "name": "Māori / iwi-linked ventures",
        "scores": {"problem": 4, "wtp": 3, "fit": 5, "speed": 2, "trust": 5, "nz_impact": 5},
        "decision": "Pilot",
        "entry": "Cultural pack (HITL cultural)",
        "skills": ["compliance-registrar", "formation-officer", "board-chief-of-staff"],
        "cultural_sensitivity": "high",
    },
    "S7": {
        "name": "Climate / cleantech grant-heavy",
        "scores": {"problem": 4, "wtp": 3, "fit": 4, "speed": 3, "trust": 4, "nz_impact": 4},
        "decision": "GO",
        "entry": "Grants + RDTI dogfood",
        "skills": ["grants-rdti-clerk", "funding-analyst", "board-chief-of-staff"],
    },
    "S8": {
        "name": "Accountants / bookkeepers (channel)",
        "scores": {"problem": 3, "wtp": 4, "fit": 3, "speed": 3, "trust": 4, "nz_impact": 3},
        "decision": "Pilot",
        "entry": "Handoff packs + referral",
        "skills": ["finance-clerk", "enterprise-adoption-officer"],
    },
    "S9": {
        "name": "Mid-market enterprise (100+)",
        "scores": {"problem": 3, "wtp": 4, "fit": 2, "speed": 1, "trust": 5, "nz_impact": 2},
        "decision": "Watch",
        "entry": "Standards mapping only pre-seed",
        "skills": ["enterprise-adoption-officer", "compliance-registrar"],
    },
    "S10": {
        "name": "Big-4 / large consultancies",
        "scores": {"problem": 2, "wtp": 5, "fit": 2, "speed": 1, "trust": 4, "nz_impact": 2},
        "decision": "Watch",
        "entry": "Complement / white-label IP later",
        "skills": ["enterprise-adoption-officer"],
    },
    "S11": {
        "name": "Telco / bank agent platforms",
        "scores": {"problem": 2, "wtp": 3, "fit": 1, "speed": 1, "trust": 3, "nz_impact": 1},
        "decision": "No",
        "entry": "Adjacent only",
        "skills": [],
    },
    "S12": {
        "name": "Local government / councils",
        "scores": {"problem": 4, "wtp": 3, "fit": 3, "speed": 1, "trust": 5, "nz_impact": 5},
        "decision": "Pilot",
        "entry": "Procurement pack + Algorithm Charter",
        "skills": ["enterprise-adoption-officer", "compliance-registrar"],
    },
}

ENTERPRISE_PRODUCTS: list[dict[str, Any]] = [
    {
        "id": "A",
        "name": "EDA fleet seats",
        "buyer": "Accelerator / EDA",
        "job": "Scale mentor capacity without hiring 10 ops staff",
        "ship": "White-label pack + partner report",
        "revenue": "Per-seat 90-day pilot → annual",
    },
    {
        "id": "B",
        "name": "RDTI evidence OS",
        "buyer": "Founder + tax advisor",
        "job": "Defensible contemporaneous R&D logs",
        "ship": "rdti + audit + board pack",
        "revenue": "Founder sub + advisor channel",
    },
    {
        "id": "C",
        "name": "Procurement trust pack",
        "buyer": "Council / gov-adjacent / mid-market",
        "job": "Answer Algorithm Charter / Privacy / HITL DD",
        "ship": "standards-mapping + compliance gate report",
        "revenue": "Paid pilot / licence",
    },
    {
        "id": "D",
        "name": "Finance handoff",
        "buyer": "SME + accountant",
        "job": "GST/invoice triage without agent email risk",
        "ship": "bank/invoice/handoff zips",
        "revenue": "Founder tier + accountant referral",
    },
    {
        "id": "E",
        "name": "Hybrid edge story",
        "buyer": "Agritech co-ops / farms",
        "job": "Local inference + founder ops narrative",
        "ship": "Portfolio link + board pack",
        "revenue": "Bundle with Byte Size Kai / SoilGuard",
    },
    {
        "id": "F",
        "name": "Investor readiness",
        "buyer": "Pre-seed founder",
        "job": "Data room + honest market claims",
        "ship": "seed pack + investor-readiness skill",
        "revenue": "Included in Active tier",
    },
    {
        "id": "G",
        "name": "Cultural sovereign stack",
        "buyer": "Iwi / Māori enterprise (gated)",
        "job": "Data sovereignty + HITL",
        "ship": "Te Mana Raraunga docs + cultural flags",
        "revenue": "Relationship-first; no cold sell",
    },
]

PORTFOLIO: list[dict[str, Any]] = [
    {"repo": "NZ-Start-Up", "total": 25, "role": "Lead product", "buyer": "EDA + founders"},
    {"repo": "Aether", "total": 21, "role": "Platform moat", "buyer": "Developers / internal"},
    {"repo": "Blue-Moon-Portal", "total": 20, "role": "Byte Size Kai (agritech lead)", "buyer": "Growers / Mana Kai"},
    {"repo": "SoilGuard-Portal", "total": 20, "role": "Whenua / pasture", "buyer": "Farms / co-ops"},
    {"repo": "fivepanelhat", "total": 19, "role": "Top-of-funnel", "buyer": "Investors / partners"},
    {"repo": "Weaver", "total": 19, "role": "Multi-tenant edge", "buyer": "Rural enterprise"},
    {"repo": "Coastal-Alpine-Core", "total": 19, "role": "Shared IP moat", "buyer": "Portfolio"},
    {"repo": "Sting-Operation-AI", "total": 19, "role": "Biosecurity wedge", "buyer": "Apiarists / MPI-adj"},
    {"repo": "whanau-preterm-support-hub", "total": 19, "role": "Social impact", "buyer": "Whānau / health"},
    {"repo": "Front_Line_Whanau", "total": 19, "role": "Frontline services", "buyer": "Whānau / NGOs"},
    {"repo": "coastal-alpine-stack", "total": 18, "role": "Architecture proof", "buyer": "Technical DD"},
    {"repo": "AquaGuard-Portal", "total": 17, "role": "Water vertical", "buyer": "Aqua / councils"},
    {"repo": "Sovereign-Edge-Firmware", "total": 17, "role": "Field layer IP", "buyer": "Hardware partners"},
    {"repo": "CAT-mail", "total": 14, "role": "Privacy utility", "buyer": "Privacy SMEs"},
]


def _total(scores: dict[str, int]) -> int:
    return sum(int(v) for v in scores.values())


def score_segment(segment_id: str) -> dict[str, Any]:
    sid = segment_id.strip().upper()
    if sid not in SEGMENTS:
        raise ValueError(f"Unknown segment '{segment_id}'. Known: {', '.join(sorted(SEGMENTS))}")
    row = dict(SEGMENTS[sid])
    scores = dict(row["scores"])
    total = _total(scores)
    row["id"] = sid
    row["total"] = total
    row["max"] = 30
    row["band"] = (
        "GO" if total >= 22 else "Pilot" if total >= 16 else "Watch" if total >= 10 else "No"
    )
    return row


def matrix_table() -> list[dict[str, Any]]:
    rows = [score_segment(sid) for sid in sorted(SEGMENTS.keys(), key=lambda s: int(s[1:]))]
    rows.sort(key=lambda r: (-r["total"], r["id"]))
    return rows


def format_matrix_markdown() -> str:
    lines = [
        "# Market-fit matrix (live)",
        "",
        "| ID | Segment | Total | Decision | Entry |",
        "|----|---------|-------|----------|-------|",
    ]
    for r in matrix_table():
        lines.append(
            f"| {r['id']} | {r['name']} | **{r['total']}**/30 | {r['decision']} | {r['entry']} |"
        )
    lines.extend(
        [
            "",
            "Bands: GO ≥22 · Pilot 16–21 · Watch 10–15 · No <10",
            "",
            "Full narrative: `docs/MARKET_FIT_MATRIX.md`",
            "",
        ]
    )
    return "\n".join(lines)


def format_enterprise_markdown() -> str:
    lines = [
        "# Enterprise adoption products (create markets)",
        "",
        "| ID | Product | Buyer | Job | Revenue |",
        "|----|---------|-------|-----|---------|",
    ]
    for p in ENTERPRISE_PRODUCTS:
        lines.append(
            f"| {p['id']} | {p['name']} | {p['buyer']} | {p['job']} | {p['revenue']} |"
        )
    lines.append("")
    return "\n".join(lines)


def format_portfolio_markdown() -> str:
    lines = [
        "# Portfolio market-fit (CAT repos)",
        "",
        "| Repo | Score /25 | Role | Buyer |",
        "|------|-----------|------|-------|",
    ]
    for p in sorted(PORTFOLIO, key=lambda x: -x["total"]):
        lines.append(f"| {p['repo']} | **{p['total']}** | {p['role']} | {p['buyer']} |")
    lines.extend(["", "Detail: `docs/PORTFOLIO_MARKET_FIT.md`", ""])
    return "\n".join(lines)


def gtm_priority() -> list[str]:
    """Top GO segments for next 90 days."""
    rows = [r for r in matrix_table() if "GO" in r["decision"].upper()]
    return [f"{r['id']} {r['name']} ({r['total']})" for r in rows[:6]]
