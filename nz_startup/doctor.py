"""Environment / install doctor for v1.0 local product."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from nz_startup import __version__
from nz_startup.paths import example_company_dir, memory_root, repo_root, skills_dir


def run_doctor() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("python", sys.version_info >= (3, 10), f"{sys.version.split()[0]} (need >=3.10)")
    add("repo_root", repo_root().is_dir(), str(repo_root()))
    skills = skills_dir()
    skill_count = len([p for p in skills.iterdir() if p.is_dir()]) if skills.is_dir() else 0
    add("skills", skill_count >= 10, f"{skill_count} skill dirs at {skills}")
    harden = skills / "agent-hardening" / "SKILL.md"
    add("agent_hardening_skill", harden.is_file(), str(harden))
    add("example_company", example_company_dir().is_dir(), str(example_company_dir()))
    add("memory_root", memory_root().is_dir(), str(memory_root()))
    add("validate_script", (repo_root() / "scripts" / "validate_skills.py").is_file(), "scripts/validate_skills.py")

    # Optional extras
    add("mcp_extra", importlib.util.find_spec("mcp") is not None, "pip install '.[mcp]' for MCP server")
    add("pypdf_extra", importlib.util.find_spec("pypdf") is not None, "pip install '.[pdf]' for PDF invoices")

    # Core modules importable
    try:
        import nz_startup.status  # noqa: F401
        import nz_startup.weekly  # noqa: F401
        import nz_startup.console  # noqa: F401

        add("core_imports", True, "status, weekly, console")
    except Exception as e:  # noqa: BLE001
        add("core_imports", False, str(e))

    soft = {"mcp_extra", "pypdf_extra", "agent_hardening_skill"}
    ok = all(c["ok"] for c in checks if c["name"] not in soft)
    return {
        "ok": ok,
        "product_version": __version__,
        "python": sys.version.split()[0],
        "checks": checks,
        "hitl": "Doctor never sends, files, or pays.",
        "next": [
            "nz-startup smoke",
            "nz-startup onboard <company>",
            "nz-startup console --port 8765",
        ]
        if ok
        else ["Fix failed checks above", "pip install -e '.[all]'"],
    }


def format_doctor_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Doctor — v{report.get('product_version')}",
        "",
        f"- Overall: **{'PASS' if report.get('ok') else 'FAIL'}**",
        f"- Python: {report.get('python')}",
        "",
    ]
    for c in report.get("checks") or []:
        mark = "OK" if c.get("ok") else "FAIL"
        # optional extras are soft
        if c.get("name") in ("mcp_extra", "pypdf_extra") and not c.get("ok"):
            mark = "OPT"
        lines.append(f"- [{mark}] **{c.get('name')}** — {c.get('detail')}")
    lines.extend(["", "## Next", ""])
    for n in report.get("next") or []:
        lines.append(f"- `{n}`")
    lines.append("")
    lines.append(report.get("hitl", ""))
    lines.append("")
    return "\n".join(lines)
