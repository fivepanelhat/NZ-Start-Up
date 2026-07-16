"""Grant / funding opportunity tracker (CSV) — draft and track only."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

FIELDS = [
    "id",
    "name",
    "funder",
    "status",
    "fit_score",
    "deadline",
    "amount_hint",
    "url",
    "next_action",
    "last_verified",
    "notes",
]

STATUSES = (
    "watch",
    "open",
    "opens_soon",
    "drafting",
    "submitted",
    "interview",
    "awarded",
    "declined",
    "closed",
    "skip",
)


def csv_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "grants-tracker.csv"


def md_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "grants-tracker.md"


def ensure_csv(company_id: str) -> Path:
    path = csv_path(company_id)
    if not path.exists() or path.stat().st_size == 0:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()
    return path


def _read_rows(company_id: str) -> list[dict[str, str]]:
    path = ensure_csv(company_id)
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_rows(company_id: str, rows: list[dict[str, str]]) -> None:
    path = ensure_csv(company_id)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    _sync_markdown(company_id, rows)


def _sync_markdown(company_id: str, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Grants tracker",
        "",
        "| ID | Name | Funder | Status | Fit | Deadline | Next action | Verified |",
        "|----|------|--------|--------|-----|----------|-------------|----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('id','')} | {r.get('name','')} | {r.get('funder','')} | "
            f"{r.get('status','')} | {r.get('fit_score','')} | {r.get('deadline','')} | "
            f"{r.get('next_action','')} | {r.get('last_verified','')} |"
        )
    lines.append("")
    lines.append("DRAFT — NOT FOR SUBMISSION. Human submits applications.")
    md_path(company_id).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _next_id(rows: list[dict[str, str]]) -> str:
    nums = []
    for r in rows:
        rid = (r.get("id") or "").strip()
        if rid.startswith("G") and rid[1:].isdigit():
            nums.append(int(rid[1:]))
    n = max(nums) + 1 if nums else 1
    return f"G{n:03d}"


def list_grants(
    company_id: str,
    *,
    status: str | None = None,
) -> list[dict[str, str]]:
    rows = _read_rows(company_id)
    if status:
        s = status.lower().strip()
        rows = [r for r in rows if (r.get("status") or "").lower() == s]
    return rows


def add_grant(
    company_id: str,
    *,
    name: str,
    funder: str = "",
    status: str = "watch",
    fit_score: str = "",
    deadline: str = "",
    amount_hint: str = "",
    url: str = "",
    next_action: str = "",
    notes: str = "",
) -> dict[str, str]:
    if not name.strip():
        raise ValueError("name is required")
    st = status.lower().strip()
    if st not in STATUSES:
        raise ValueError(f"Invalid status. Allowed: {', '.join(STATUSES)}")
    if fit_score:
        try:
            score = int(fit_score)
            if score < 0 or score > 100:
                raise ValueError
        except ValueError as e:
            raise ValueError("fit_score must be integer 0-100") from e
    rows = _read_rows(company_id)
    row = {
        "id": _next_id(rows),
        "name": name.strip(),
        "funder": funder.strip(),
        "status": st,
        "fit_score": str(fit_score).strip(),
        "deadline": deadline.strip(),
        "amount_hint": amount_hint.strip(),
        "url": url.strip(),
        "next_action": next_action.strip(),
        "last_verified": date.today().isoformat(),
        "notes": notes.strip(),
    }
    rows.append(row)
    _write_rows(company_id, rows)
    append_audit(
        ensure_exists(company_id),
        actor="agent:grants-rdti-clerk",
        skill="grants-rdti-clerk",
        action="grants_add",
        summary=f"{row['id']} {row['name']} [{row['status']}]",
        artefact_ref="grants-tracker.csv",
        tier="gold",
        hitl_required=st == "submitted",
        hitl_status="n/a" if st != "submitted" else "pending",
    )
    return row


def update_grant(
    company_id: str,
    grant_id: str,
    *,
    status: str | None = None,
    fit_score: str | None = None,
    deadline: str | None = None,
    next_action: str | None = None,
    notes: str | None = None,
    url: str | None = None,
    verify: bool = True,
) -> dict[str, str]:
    rows = _read_rows(company_id)
    found = None
    for r in rows:
        if r.get("id") == grant_id:
            found = r
            break
    if not found:
        raise FileNotFoundError(f"Unknown grant id: {grant_id}")
    if status is not None:
        st = status.lower().strip()
        if st not in STATUSES:
            raise ValueError(f"Invalid status. Allowed: {', '.join(STATUSES)}")
        if st == "submitted":
            # Agents must not claim submission without HITL note
            found["status"] = st
            found["notes"] = (
                (found.get("notes") or "")
                + " | STATUS submitted — confirm human actually submitted portal."
            ).strip(" |")
        else:
            found["status"] = st
    if fit_score is not None:
        if fit_score != "":
            score = int(fit_score)
            if score < 0 or score > 100:
                raise ValueError("fit_score must be 0-100")
        found["fit_score"] = str(fit_score)
    if deadline is not None:
        found["deadline"] = deadline
    if next_action is not None:
        found["next_action"] = next_action
    if notes is not None:
        found["notes"] = notes
    if url is not None:
        found["url"] = url
    if verify:
        found["last_verified"] = date.today().isoformat()
    _write_rows(company_id, rows)
    append_audit(
        ensure_exists(company_id),
        actor="agent:grants-rdti-clerk",
        skill="grants-rdti-clerk",
        action="grants_update",
        summary=f"{grant_id} → {found.get('status')} fit={found.get('fit_score')}",
        artefact_ref="grants-tracker.csv",
        tier="gold",
        hitl_required=found.get("status") == "submitted",
        hitl_status="pending" if found.get("status") == "submitted" else "n/a",
    )
    return found


def rank_by_fit(company_id: str, *, min_score: int = 0) -> list[dict[str, str]]:
    rows = list_grants(company_id)
    scored = []
    for r in rows:
        if (r.get("status") or "") in ("closed", "skip", "declined"):
            continue
        try:
            score = int(r.get("fit_score") or 0)
        except ValueError:
            score = 0
        if score >= min_score:
            scored.append(r)
    scored.sort(key=lambda r: int(r.get("fit_score") or 0), reverse=True)
    return scored


def seed_nz_starters(company_id: str) -> list[dict[str, str]]:
    """Seed illustrative NZ opportunities — re-verify before acting."""
    if _read_rows(company_id):
        return []
    starters = [
        {
            "name": "RDTI — Research & Development Tax Incentive",
            "funder": "Inland Revenue / MBIE",
            "status": "watch",
            "fit_score": "85",
            "deadline": "ongoing",
            "url": "https://www.rdti.govt.nz/",
            "next_action": "Keep contemporaneous activity log",
            "notes": "Not cash-in-bank; logging habit is product-critical",
        },
        {
            "name": "Regional EDA ScaleUp-style grant (verify local name)",
            "funder": "Regional EDA e.g. Venture Taranaki",
            "status": "watch",
            "fit_score": "70",
            "deadline": "TBD",
            "next_action": "Confirm current programme with Nick / EDA advisor",
            "notes": "Landscape moves post-Callaghan — re-verify",
        },
        {
            "name": "Accelerator cohort (PowerUp / Sprout / Icehouse — pick fit)",
            "funder": "Accelerator network",
            "status": "watch",
            "fit_score": "60",
            "deadline": "TBD",
            "next_action": "Check next cohort window",
        },
    ]
    out = []
    for s in starters:
        out.append(add_grant(company_id, **s))
    return out


def format_board_slice(company_id: str) -> str:
    rows = rank_by_fit(company_id)
    lines = ["### Grants (top fit)", ""]
    if not rows:
        lines.append("_No grants tracked — run grants seed or add._")
    for r in rows[:5]:
        lines.append(
            f"- `{r.get('id')}` **{r.get('name')}** fit={r.get('fit_score')} "
            f"[{r.get('status')}] — {r.get('next_action') or '—'}"
        )
    lines.append("")
    lines.append("Human submits. Agent drafts only.")
    return "\n".join(lines)
