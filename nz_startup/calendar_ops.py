"""Compliance and ops calendar with deadline reminders."""
from __future__ import annotations

import csv
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

FIELDS = [
    "id",
    "due",
    "item",
    "owner",
    "status",
    "category",
    "recurring",
    "notes",
]

STATUSES = ("planned", "in_progress", "done", "blocked", "cancelled")
CATEGORIES = (
    "compliance",
    "finance",
    "rdti",
    "gtm",
    "legal",
    "ops",
    "board",
    "other",
)


def csv_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "calendar.csv"


def md_path(company_id: str) -> Path:
    return ensure_exists(company_id) / "calendar.md"


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
        "# Compliance Calendar",
        "",
        "| ID | Due | Item | Owner | Status | Category |",
        "|----|-----|------|-------|--------|----------|",
    ]
    for r in sorted(rows, key=lambda x: x.get("due") or "9999"):
        lines.append(
            f"| {r.get('id','')} | {r.get('due','')} | {r.get('item','')} | "
            f"{r.get('owner','')} | {r.get('status','')} | {r.get('category','')} |"
        )
    lines.append("")
    lines.append("INFORMATION ONLY — not a compliance certificate.")
    md_path(company_id).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _next_id(rows: list[dict[str, str]]) -> str:
    nums = []
    for r in rows:
        rid = (r.get("id") or "").strip()
        if rid.startswith("C") and rid[1:].isdigit():
            nums.append(int(rid[1:]))
    n = max(nums) + 1 if nums else 1
    return f"C{n:03d}"


def _parse_due(due: str) -> date | None:
    due = (due or "").strip()
    if not due or due.upper() in ("TBD", "WEEKLY", "ONGOING", "N/A"):
        return None
    try:
        return date.fromisoformat(due[:10])
    except ValueError:
        return None


def add_item(
    company_id: str,
    *,
    item: str,
    due: str,
    owner: str = "Founder",
    status: str = "planned",
    category: str = "compliance",
    recurring: str = "",
    notes: str = "",
) -> dict[str, str]:
    if not item.strip():
        raise ValueError("item is required")
    status_l = status.lower().strip()
    if status_l not in STATUSES:
        raise ValueError(f"Invalid status. Allowed: {', '.join(STATUSES)}")
    cat = category.lower().strip()
    if cat not in CATEGORIES:
        raise ValueError(f"Invalid category. Allowed: {', '.join(CATEGORIES)}")
    rows = _read_rows(company_id)
    row = {
        "id": _next_id(rows),
        "due": due.strip(),
        "item": item.strip(),
        "owner": owner.strip() or "Founder",
        "status": status_l,
        "category": cat,
        "recurring": recurring.strip(),
        "notes": notes.strip(),
    }
    rows.append(row)
    _write_rows(company_id, rows)
    append_audit(
        ensure_exists(company_id),
        actor="agent:compliance-registrar",
        skill="compliance-registrar",
        action="calendar_add",
        summary=f"{row['id']} due {row['due']}: {row['item'][:80]}",
        artefact_ref="calendar.csv",
        tier="gold",
    )
    return row


def update_item(
    company_id: str,
    item_id: str,
    *,
    due: str | None = None,
    status: str | None = None,
    owner: str | None = None,
    notes: str | None = None,
    item: str | None = None,
) -> dict[str, str]:
    rows = _read_rows(company_id)
    found = None
    for r in rows:
        if r.get("id") == item_id:
            found = r
            break
    if not found:
        raise FileNotFoundError(f"Unknown calendar id: {item_id}")
    if due is not None:
        found["due"] = due
    if status is not None:
        st = status.lower().strip()
        if st not in STATUSES:
            raise ValueError(f"Invalid status. Allowed: {', '.join(STATUSES)}")
        found["status"] = st
    if owner is not None:
        found["owner"] = owner
    if notes is not None:
        found["notes"] = notes
    if item is not None:
        found["item"] = item
    _write_rows(company_id, rows)
    append_audit(
        ensure_exists(company_id),
        actor="agent:compliance-registrar",
        skill="compliance-registrar",
        action="calendar_update",
        summary=f"{item_id} → {found.get('status')} due {found.get('due')}",
        artefact_ref="calendar.csv",
        tier="gold",
    )
    return found


def list_items(company_id: str, *, status: str | None = None) -> list[dict[str, str]]:
    rows = _read_rows(company_id)
    if status:
        s = status.lower().strip()
        rows = [r for r in rows if (r.get("status") or "").lower() == s]
    return rows


def reminders(
    company_id: str,
    *,
    within_days: int = 14,
    include_overdue: bool = True,
    as_of: date | None = None,
) -> dict[str, Any]:
    """Return upcoming and overdue dated items (status not done/cancelled)."""
    today = as_of or date.today()
    horizon = today + timedelta(days=max(0, within_days))
    upcoming: list[dict[str, Any]] = []
    overdue: list[dict[str, Any]] = []
    undated: list[dict[str, str]] = []

    for r in _read_rows(company_id):
        if (r.get("status") or "").lower() in ("done", "cancelled"):
            continue
        d = _parse_due(r.get("due", ""))
        if d is None:
            undated.append(r)
            continue
        days = (d - today).days
        enriched = {**r, "days_until": days, "due_parsed": d.isoformat()}
        if d < today and include_overdue:
            overdue.append(enriched)
        elif today <= d <= horizon:
            upcoming.append(enriched)

    overdue.sort(key=lambda x: x.get("due_parsed") or "")
    upcoming.sort(key=lambda x: x.get("due_parsed") or "")
    return {
        "as_of": today.isoformat(),
        "within_days": within_days,
        "overdue": overdue,
        "upcoming": upcoming,
        "undated_open": undated,
        "count_actionable": len(overdue) + len(upcoming),
    }


def format_reminders_markdown(company_id: str, *, within_days: int = 14) -> str:
    data = reminders(company_id, within_days=within_days)
    lines = [
        f"# Deadline reminders (next {within_days} days)",
        "",
        f"- As of: {data['as_of']}",
        f"- Actionable dated items: {data['count_actionable']}",
        "",
        "## Overdue",
        "",
    ]
    if not data["overdue"]:
        lines.append("_None_")
    for r in data["overdue"]:
        lines.append(
            f"- ⚠️ `{r.get('id')}` **{r.get('item')}** — due {r.get('due')} "
            f"({r.get('days_until')}d) · {r.get('owner')} · {r.get('status')}"
        )
    lines.extend(["", "## Upcoming", ""])
    if not data["upcoming"]:
        lines.append("_None in window_")
    for r in data["upcoming"]:
        lines.append(
            f"- `{r.get('id')}` **{r.get('item')}** — due {r.get('due')} "
            f"({r.get('days_until')}d) · {r.get('owner')} · {r.get('category')}"
        )
    lines.extend(["", "## Open undated / recurring", ""])
    for r in data["undated_open"][:20]:
        lines.append(
            f"- `{r.get('id')}` {r.get('item')} · due note: {r.get('due')} · "
            f"{r.get('recurring') or '—'}"
        )
    lines.append("")
    lines.append("INFORMATION ONLY — not a compliance certificate. Human acts on filings.")
    return "\n".join(lines)


def seed_defaults(company_id: str) -> list[dict[str, str]]:
    """Seed common NZ founder deadlines if calendar empty."""
    if _read_rows(company_id):
        return []
    seeds = [
        {
            "item": "Incorporate NZ limited company",
            "due": "TBD",
            "category": "compliance",
            "notes": "Founder files via RealMe",
        },
        {
            "item": "IRD number + GST registration decision",
            "due": "TBD",
            "category": "finance",
        },
        {
            "item": "Weekly board operating review",
            "due": "Weekly",
            "category": "board",
            "recurring": "weekly",
        },
        {
            "item": "RDTI contemporaneous activity log",
            "due": "Ongoing",
            "category": "rdti",
            "recurring": "ongoing",
            "owner": "grants-rdti-clerk",
        },
    ]
    out = []
    for s in seeds:
        out.append(
            add_item(
                company_id,
                item=s["item"],
                due=s["due"],
                category=s.get("category", "compliance"),
                recurring=s.get("recurring", ""),
                owner=s.get("owner", "Founder"),
                notes=s.get("notes", ""),
            )
        )
    return out
