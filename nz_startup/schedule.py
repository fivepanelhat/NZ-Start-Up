"""G6 — OS-native cadence install (Task Scheduler / launchd / systemd).

Never emails. Jobs write HITL-safe artefacts to company memory only.
"""
from __future__ import annotations

import platform
import shlex
import sys
from pathlib import Path
from typing import Any

from nz_startup.paths import repo_root

TASK_NAME = "NZ-Startup-WeeklyCadence"
LAUNCHD_LABEL = "nz.startup.weekly"
SYSTEMD_UNIT = "nz-startup-weekly"


def _python() -> str:
    return sys.executable


def _runner_script() -> Path:
    """Write a small runner that invokes weekly + board + export for all companies."""
    root = repo_root()
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    path = scripts / "run_cadence.py"
    path.write_text(
        '''#!/usr/bin/env python3
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
''',
        encoding="utf-8",
        newline="\n",
    )
    return path


def install_schedule(*, force: bool = False) -> dict[str, Any]:
    """Register OS-native weekly timer. Returns instructions + artefacts."""
    runner = _runner_script()
    system = platform.system().lower()
    py = _python()
    result: dict[str, Any] = {
        "platform": system,
        "runner": str(runner),
        "python": py,
        "hitl": "Cadence writes local artefacts only — never emails or files government forms.",
    }

    if system == "windows":
        # schtasks XML-free simple weekly Sunday 09:00 local
        cmd = (
            f'schtasks /Create /F /TN "{TASK_NAME}" /SC WEEKLY /D SUN /ST 09:00 '
            f'/TR "\\"{py}\\" \\"{runner}\\"" /RL LIMITED'
        )
        result["command"] = cmd
        result["uninstall"] = f'schtasks /Delete /F /TN "{TASK_NAME}"'
        result["note"] = (
            "Run the command in an elevated PowerShell if Task Scheduler denies access. "
            "Or paste into Task Scheduler GUI: Weekly · Sunday 09:00 · action = python run_cadence.py"
        )
        # Attempt non-elevated create
        import subprocess

        try:
            proc = subprocess.run(
                [
                    "schtasks",
                    "/Create",
                    "/F" if force else "/F",
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

    # Linux systemd user unit
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
    result["note"] = "Run enable command if systemd user session is available."
    return result


def uninstall_schedule() -> dict[str, Any]:
    system = platform.system().lower()
    result: dict[str, Any] = {"platform": system}
    if system == "windows":
        import subprocess

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
        result["plist"] = str(plist)
        result["removed"] = False
        result["manual"] = f"launchctl unload {plist} && rm {plist}"
        return result
    result["manual"] = f"systemctl --user disable --now {SYSTEMD_UNIT}.timer"
    return result


def schedule_status() -> dict[str, Any]:
    runner = repo_root() / "scripts" / "run_cadence.py"
    return {
        "runner_exists": runner.is_file(),
        "runner": str(runner),
        "platform": platform.system(),
        "task_name_windows": TASK_NAME,
        "launchd_label": LAUNCHD_LABEL,
        "systemd_unit": SYSTEMD_UNIT,
    }
