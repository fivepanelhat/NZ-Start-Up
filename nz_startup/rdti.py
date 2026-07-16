"""Contemporaneous RDTI activity log helpers."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

FIELDS = [
 "date",
 "hours",
 "activity",
 "technical_uncertainty",
 "evidence_ref",
 "person",
 "notes",
]


def log_path(company_id: str) -> Path:
 return ensure_exists(company_id) / "rdti-log.csv"


def ensure_header(path: Path) -> None:
 if not path.exists() or path.stat().st_size == 0:
 path.parent.mkdir(parents=True, exist_ok=True)
 with path.open("w", encoding="utf-8", newline="") as f:
 csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def append_entry(
 company_id: str,
 *,
 hours: float,
 activity: str,
 technical_uncertainty: str,
 evidence_ref: str,
 person: str = "Founder",
 notes: str = "",
 entry_date: str | None = None,
) -> dict:
 if hours <= 0:
 raise ValueError("hours must be positive - never invent time")
 if not activity.strip():
 raise ValueError("activity is required")
 if not technical_uncertainty.strip():
 raise ValueError("technical_uncertainty is required for RDTI character")
 if not evidence_ref.strip():
 raise ValueError("evidence_ref required (commit, timesheet, doc id)")

 path = log_path(company_id)
 ensure_header(path)
 row = {
 "date": entry_date or date.today().isoformat(),
 "hours": f"{float(hours):.2f}",
 "activity": activity.strip(),
 "technical_uncertainty": technical_uncertainty.strip(),
 "evidence_ref": evidence_ref.strip(),
 "person": person.strip() or "Founder",
 "notes": notes.strip(),
 }
 with path.open("a", encoding="utf-8", newline="") as f:
 csv.DictWriter(f, fieldnames=FIELDS).writerow(row)
 append_audit(
 ensure_exists(company_id),
 actor="agent:grants-rdti-clerk",
 skill="grants-rdti-clerk",
 action="append_rdti_log",
 summary=f"{row['hours']}h - {row['activity'][:80]}",
 artefact_ref="rdti-log.csv",
 tier="platinum",
 )
 return row


def list_entries(company_id: str, limit: int = 50) -> list[dict]:
 path = log_path(company_id)
 if not path.exists():
 return []
 with path.open(encoding="utf-8", newline="") as f:
 rows = list(csv.DictReader(f))
 return rows[-limit:]
