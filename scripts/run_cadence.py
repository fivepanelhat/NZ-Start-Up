#!/usr/bin/env python3
"""Weekly cadence: status, weekly board, deadline export, INDEX refresh. HITL-safe."""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo importable when launched from OS scheduler
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nz_startup import board_pack, export_reminders, memory, status, weekly
from nz_startup.memory_index import write_index
from nz_startup.audit import append_audit


def main() -> int:
    companies = memory.list_companies()
    if not companies:
        print("No companies in memory — nothing to run.")
        return 0
    for cid in companies:
        try:
            status.write_status(cid)
            weekly.generate_weekly_review(cid)
            export_reminders.export_all(cid)
            write_index(cid)
            append_audit(
                memory.ensure_exists(cid),
                actor="scheduler:cadence",
                skill="board-chief-of-staff",
                action="schedule_weekly_cadence",
                summary="OS timer cadence: status + weekly + export + INDEX",
                model_tier="light",
                outcome="ok",
            )
            print(f"ok: {cid}")
        except Exception as e:  # noqa: BLE001
            print(f"error: {cid}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
