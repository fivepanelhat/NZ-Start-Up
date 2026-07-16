"""G10 - Company INDEX.md + compaction + single-writer rule."""
from __future__ import annotations

import json
import os
import time
from datetime import date
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit, sum_costs
from nz_startup.memory import ensure_exists

LOCK_NAME = ".memory.lock"
SINGLE_WRITER_DOC = """
## Single-writer rule

Only **one** agent or human session may write to a company memory tree at a time.
Acquire `.memory.lock` via the runtime before multi-file updates; release when done.
Concurrent writers cause classic multi-agent file-race corruption.
"""


class MemoryLock:
 def __init__(self, company_id: str, *, timeout_s: float = 30.0):
 self.company_id = company_id
 self.path = ensure_exists(company_id) / LOCK_NAME
 self.timeout_s = timeout_s
 self._held = False

 def __enter__(self) -> "MemoryLock":
 start = time.time()
 while True:
 try:
 fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
 with os.fdopen(fd, "w", encoding="utf-8") as f:
 f.write(
 json.dumps(
 {
 "pid": os.getpid(),
 "ts": date.today().isoformat(),
 "company_id": self.company_id,
 }
 )
 )
 self._held = True
 return self
 except FileExistsError:
 if time.time() - start > self.timeout_s:
 try:
 age = time.time() - self.path.stat().st_mtime
 if age > 3600:
 self.path.unlink(missing_ok=True)
 continue
 except OSError:
 pass
 raise TimeoutError(f"Memory lock busy: {self.path}")
 time.sleep(0.05)

 def __exit__(self, *args: Any) -> None:
 if self._held:
 try:
 self.path.unlink(missing_ok=True)
 except OSError:
 pass
 self._held = False


def write_index(company_id: str) -> Path:
 """Small INDEX.md - the only default context load for Board skill."""
 company = ensure_exists(company_id)
 costs = sum_costs(company)
 lines = [
 f"# INDEX - {company_id}",
 "",
 f"Updated: {date.today().isoformat()}",
 "",
 "## Load by default",
 "",
 "- `profile.md`",
 "- `tasks.md` / `tasks.jsonl`",
 "- `pipeline.md`",
 "- `calendar.md` (or reminders)",
 "- `status/status-latest.md`",
 "- latest `weekly/*.md`",
 "",
 "## Just-in-time (do not preload)",
 "",
 "- `finance/**`",
 "- `drafts/**`",
 "- `commercial/**`",
 "- full `audit.jsonl`",
 "- archived weekly reports",
 "",
 "## Fleet cost (telemetry)",
 "",
 f"- Audit entries with cost: {costs.get('entries')}",
 f"- Est. fleet cost (NZD, heuristic): **${costs.get('est_cost_nzd')}**",
 "",
 SINGLE_WRITER_DOC,
 "",
 ]
 path = company / "INDEX.md"
 path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
 return path


def compact_memory(company_id: str) -> dict[str, Any]:
 """
 Monthly compaction ritual (deterministic):
 - ensure INDEX
 - archive weekly files older than 60 days into weekly/archive/
 - note in decisions.md
 """
 company = ensure_exists(company_id)
 archived = 0
 weekly = company / "weekly"
 arch = weekly / "archive"
 if weekly.is_dir():
 arch.mkdir(exist_ok=True)
 today = date.today()
 for p in weekly.glob("*.md"):
 stem = p.stem[:10]
 try:
 d = date.fromisoformat(stem)
 except ValueError:
 continue
 if (today - d).days > 60:
 dest = arch / p.name
 p.replace(dest)
 archived += 1
 idx = write_index(company_id)
 decisions = company / "decisions.md"
 line = (
 f"- {date.today().isoformat()} - Memory compaction: "
 f"archived {archived} weekly files; INDEX refreshed.\n"
 )
 if decisions.exists():
 with decisions.open("a", encoding="utf-8") as f:
 f.write(line)
 else:
 decisions.write_text("# Decisions\n\n" + line, encoding="utf-8")
 append_audit(
 company,
 actor="agent:board-chief-of-staff",
 skill="board-chief-of-staff",
 action="memory_compact",
 summary=f"Archived {archived} weekly files",
 artefact_ref="INDEX.md",
 model_tier="light",
 outcome="ok",
 )
 return {"archived_weekly": archived, "index": str(idx)}
