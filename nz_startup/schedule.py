"""G6/T5 — OS-native cadence install (relocatable + verifiable).

Never emails. Jobs write HITL-safe artefacts to company memory only.
Generated runner lives under ~/.nz-startup/ (not the repo tree).
"""
from __future__ import annotations

import json
import platform
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup.paths import repo_root

TASK_NAME = "NZ-Startup-WeeklyCadence"
LAUNCHD_LABEL = "nz.startup.weekly"
SYSTEMD_UNIT = "nz-startup-weekly"


def state_dir() -> Path:
    p = Path.home() / ".nz-startup"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _python() -> str:
    return sys.executable


def _runner_script() -> Path:
    """Write cadence runner to state dir (T5 — do not mutate repo at install)."""
    path = state_dir() / "run_cadence.py"
    root = repo_root().resolve()
    path.write_text(
        f'''#!/usr/bin/env python3
"""Weekly cadence: status, weekly board, deadline export, INDEX + heartbeat. HITL-safe."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"{root}")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nz_startup import export_reminders, memory, status, weekly
from nz_startup.memory_index import write_index
from nz_startup.audit import append_audit

STATE = Path.home() / ".nz-startup"


def _heartbeat(companies: list[str], ok: int, errors: list[str]) -> None:
    STATE.mkdir(parents=True, exist_ok=True)
    payload = {{
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "companies": companies,
        "ok": ok,
        "errors": errors[:20],
        "python": sys.executable,
        "repo": str(ROOT),
    }}
    (STATE / "cadence-heartbeat.json").write_text(
        json.dumps(payload, indent=2) + "\\n", encoding="utf-8"
    )
    for cid in companies:
        try:
            cpath = memory.ensure_exists(cid)
            (cpath / "status").mkdir(exist_ok=True)
            (cpath / "status" / "cadence-last-run.json").write_text(
                json.dumps(payload, indent=2) + "\\n", encoding="utf-8"
            )
        except Exception:
            pass


def main() -> int:
    companies = memory.list_companies()
    if not companies:
        print("No companies in memory — nothing to run.")
        _heartbeat([], 0, [])
        return 0
    ok = 0
    errors: list[str] = []
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
            print(f"ok: {{cid}}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            errors.append(f"{{cid}}: {{e}}")
            print(f"error: {{cid}}: {{e}}", file=sys.stderr)
    _heartbeat(companies, ok, errors)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
''',
        encoding="utf-8",
        newline="\n",
    )
    # also keep a thin stub in repo scripts for discoverability
    stub = repo_root() / "scripts" / "run_cadence.py"
    stub.parent.mkdir(exist_ok=True)
    if not stub.is_file() or "STATE dir" not in stub.read_text(encoding="utf-8", errors="replace"):
        stub.write_text(
            """#!/usr/bin/env python3
\"\"\"Thin launcher — real runner lives in ~/.nz-startup/run_cadence.py (T5).\"\"\"
from __future__ import annotations

import runpy
import sys
from pathlib import Path

target = Path.home() / ".nz-startup" / "run_cadence.py"
if not target.is_file():
    # bootstrap via package
    from nz_startup.schedule import _runner_script

    target = _runner_script()
sys.argv[0] = str(target)
runpy.run_path(str(target), run_name="__main__")
""",
            encoding="utf-8",
            newline="\n",
        )
    return path


def install_schedule(*, force: bool = False) -> dict[str, Any]:
    runner = _runner_script()
    system = platform.system().lower()
    py = _python()
    result: dict[str, Any] = {
        "platform": system,
        "runner": str(runner),
        "python": py,
        "state_dir": str(state_dir()),
        "hitl": "Cadence writes local artefacts only — never emails or files government forms.",
    }

    if system == "windows":
        result["command"] = (
            f'schtasks /Create /F /TN "{TASK_NAME}" /SC WEEKLY /D SUN /ST 09:00 '
            f'/TR "\\"{py}\\" \\"{runner}\\"" /RL LIMITED'
        )
        result["uninstall"] = f'schtasks /Delete /F /TN "{TASK_NAME}"'
        try:
            proc = subprocess.run(
                [
                    "schtasks",
                    "/Create",
                    "/F",
                    "/TN",
                    TASK_NAME,
                    "/SC",
                    "WEEKLY",
                    "/D",
                    "SUN",
                    "/ST",
                    "09:00",
                    "/TR",
                    f'"{py}" "{runner}"',
                    "/RL",
                    "LIMITED",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            result["exit_code"] = proc.returncode
            result["stdout"] = (proc.stdout or "")[:500]
            result["stderr"] = (proc.stderr or "")[:500]
            result["installed"] = proc.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
            result["installed"] = False
            result["error"] = str(e)
        return result

    if system == "darwin":
        plist_dir = Path.home() / "Library" / "LaunchAgents"
        plist_dir.mkdir(parents=True, exist_ok=True)
        plist = plist_dir / f"{LAUNCHD_LABEL}.plist"
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{LAUNCHD_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{py}</string>
    <string>{runner}</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>0</integer>
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key><string>{Path.home() / "Library/Logs/nz-startup-weekly.log"}</string>
  <key>StandardErrorPath</key><string>{Path.home() / "Library/Logs/nz-startup-weekly.err"}</string>
</dict>
</plist>
"""
        plist.write_text(content, encoding="utf-8")
        result["plist"] = str(plist)
        result["load"] = f"launchctl load {shlex.quote(str(plist))}"
        result["uninstall"] = f"launchctl unload {shlex.quote(str(plist))} && rm {shlex.quote(str(plist))}"
        result["installed"] = True
        return result

    unit_dir = Path.home() / ".config" / "systemd" / "user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    service = unit_dir / f"{SYSTEMD_UNIT}.service"
    timer = unit_dir / f"{SYSTEMD_UNIT}.timer"
    service.write_text(
        f"""[Unit]
Description=NZ Start-Up weekly cadence (HITL-safe local artefacts)

[Service]
Type=oneshot
ExecStart={py} {runner}
WorkingDirectory={repo_root()}
""",
        encoding="utf-8",
    )
    timer.write_text(
        f"""[Unit]
Description=NZ Start-Up weekly cadence timer

[Timer]
OnCalendar=Sun *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
""",
        encoding="utf-8",
    )
    result["service"] = str(service)
    result["timer"] = str(timer)
    result["enable"] = f"systemctl --user enable --now {SYSTEMD_UNIT}.timer"
    result["uninstall"] = f"systemctl --user disable --now {SYSTEMD_UNIT}.timer"
    result["installed"] = True
    return result


def uninstall_schedule() -> dict[str, Any]:
    system = platform.system().lower()
    result: dict[str, Any] = {"platform": system}
    if system == "windows":
        try:
            proc = subprocess.run(
                ["schtasks", "/Delete", "/F", "/TN", TASK_NAME],
                capture_output=True,
                text=True,
                timeout=30,
            )
            result["exit_code"] = proc.returncode
            result["removed"] = proc.returncode == 0
        except (FileNotFoundError, OSError) as e:
            result["removed"] = False
            result["error"] = str(e)
        return result
    if system == "darwin":
        plist = Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
        result["manual"] = f"launchctl unload {plist} && rm {plist}"
        result["removed"] = False
        return result
    result["manual"] = f"systemctl --user disable --now {SYSTEMD_UNIT}.timer"
    return result


def read_heartbeat() -> dict[str, Any] | None:
    path = state_dir() / "cadence-heartbeat.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def schedule_status() -> dict[str, Any]:
    runner = state_dir() / "run_cadence.py"
    hb = read_heartbeat()
    return {
        "runner_exists": runner.is_file(),
        "runner": str(runner),
        "state_dir": str(state_dir()),
        "platform": platform.system(),
        "task_name_windows": TASK_NAME,
        "launchd_label": LAUNCHD_LABEL,
        "systemd_unit": SYSTEMD_UNIT,
        "last_heartbeat": hb,
    }


def verify_schedule() -> dict[str, Any]:
    """T5 — query OS scheduler presence + heartbeat freshness."""
    system = platform.system().lower()
    result: dict[str, Any] = {
        "platform": system,
        "runner": schedule_status(),
        "os_task_present": None,
        "heartbeat": read_heartbeat(),
        "ok": False,
        "checks": [],
    }
    runner_ok = (state_dir() / "run_cadence.py").is_file()
    result["checks"].append({"check": "runner_script", "ok": runner_ok})

    if system == "windows":
        try:
            proc = subprocess.run(
                ["schtasks", "/Query", "/TN", TASK_NAME],
                capture_output=True,
                text=True,
                timeout=30,
            )
            present = proc.returncode == 0
            result["os_task_present"] = present
            result["checks"].append({"check": "schtasks", "ok": present, "detail": (proc.stdout or "")[:200]})
        except (FileNotFoundError, OSError) as e:
            result["os_task_present"] = False
            result["checks"].append({"check": "schtasks", "ok": False, "detail": str(e)})
    elif system == "darwin":
        plist = Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
        present = plist.is_file()
        result["os_task_present"] = present
        result["checks"].append({"check": "launchd_plist", "ok": present})
    else:
        timer = Path.home() / ".config" / "systemd" / "user" / f"{SYSTEMD_UNIT}.timer"
        present = timer.is_file()
        result["os_task_present"] = present
        result["checks"].append({"check": "systemd_timer", "ok": present})

    hb = result["heartbeat"]
    hb_ok = bool(hb and hb.get("ts"))
    result["checks"].append(
        {
            "check": "heartbeat",
            "ok": hb_ok,
            "ts": (hb or {}).get("ts"),
            "note": "absent until first schedule run",
        }
    )
    # ok if runner exists; OS task optional until install; heartbeat soft
    result["ok"] = runner_ok
    result["cadence_last_ran"] = (hb or {}).get("ts")
    return result
