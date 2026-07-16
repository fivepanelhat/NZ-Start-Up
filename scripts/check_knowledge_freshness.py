#!/usr/bin/env python3
"""G4 - Fail CI when knowledge/*.md verified date is > max_age_days stale."""
from __future__ import annotations

import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
# Also freshness-check procurement collateral (final review: stale standards doc is worse than none)
EXTRA_FILES = [
 ROOT / "compliance" / "standards-mapping.md",
]
MAX_AGE_DAYS = 90
VERIFIED_RE = re.compile(
 r"(?im)^(?:verified|verified_on|last_verified)\s*:\s*['\"]?(\d{4}-\d{2}-\d{2})"
)


def parse_verified(text: str) -> date | None:
 m = VERIFIED_RE.search(text)
 if not m:
 # also accept HTML/comment form
 m2 = re.search(r"verified[:\s]+(\d{4}-\d{2}-\d{2})", text, re.I)
 if not m2:
 return None
 return date.fromisoformat(m2.group(1))
 return date.fromisoformat(m.group(1))


def main() -> int:
 if not KNOWLEDGE.is_dir():
 print("error: knowledge/ missing", file=sys.stderr)
 return 2
 today = date.today()
 failures: list[str] = []
 ok_files: list[str] = []
 paths = list(sorted(KNOWLEDGE.glob("*.md"))) + [p for p in EXTRA_FILES if p.is_file()]
 for path in paths:
 try:
 rel = path.relative_to(ROOT).as_posix()
 except ValueError:
 rel = path.name
 text = path.read_text(encoding="utf-8", errors="replace")
 verified = parse_verified(text)
 if verified is None:
 failures.append(f"{rel}: missing verified: YYYY-MM-DD frontmatter")
 continue
 age = (today - verified).days
 if age > MAX_AGE_DAYS:
 failures.append(
 f"{rel}: verified {verified.isoformat()} is {age}d old "
 f"(max {MAX_AGE_DAYS}d) - re-verify"
 )
 else:
 ok_files.append(f"{rel}: verified {verified.isoformat()} ({age}d)")
 print("Knowledge freshness check")
 print(f"Max age: {MAX_AGE_DAYS} days | Today: {today.isoformat()}")
 for line in ok_files:
 print(f" OK {line}")
 for line in failures:
 print(f" FAIL {line}", file=sys.stderr)
 if failures:
 print(f"\n{len(failures)} knowledge file(s) stale or missing verified date.", file=sys.stderr)
 return 1
 print(f"\nAll {len(ok_files)} knowledge files fresh.")
 return 0


if __name__ == "__main__":
 raise SystemExit(main())
