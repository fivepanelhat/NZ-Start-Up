"""
Hardened compliance gate — machine-readable pass/fail for product controls.

Does not certify legal compliance of a founder's business. Checks product controls.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup import __version__
from nz_startup.hitl import FORBIDDEN_TOOL_NAMES
from nz_startup.paths import company_dir, repo_root, skills_dir


def _ok(name: str, passed: bool, detail: str, severity: str = "hard") -> dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "detail": detail,
        "severity": severity,  # hard | soft
    }


def run_compliance_check(company_id: str | None = None) -> dict[str, Any]:
    root = repo_root()
    checks: list[dict[str, Any]] = []

    # Licence proprietary
    license_text = ""
    lic = root / "LICENSE"
    if lic.is_file():
        license_text = lic.read_text(encoding="utf-8", errors="replace")
    is_prop = "PROPRIETARY" in license_text.upper() and "Apache License" not in license_text
    checks.append(
        _ok(
            "proprietary_license",
            is_prop,
            "LICENSE is Coastal Alpine Tech proprietary"
            if is_prop
            else "LICENSE missing proprietary markers or still Apache",
        )
    )
    notice = root / "NOTICE"
    checks.append(
        _ok(
            "notice_proprietary",
            notice.is_file()
            and "PROPRIETARY" in notice.read_text(encoding="utf-8", errors="replace").upper(),
            "NOTICE declares proprietary",
        )
    )

    # Compliance docs
    required_docs = [
        "COMPLIANCE.md",
        "SECURITY.md",
        "compliance/hitl-matrix.md",
        "compliance/legal-boundaries-nz.md",
        "compliance/privacy-act-2020.md",
        "compliance/te-mana-raraunga.md",
        "compliance/audit-log-schema.md",
        "docs/AGENT_HARDENING.md",
    ]
    for rel in required_docs:
        p = root / rel
        checks.append(_ok(f"doc:{rel}", p.is_file(), str(p)))

    # Hardening code + skill
    checks.append(
        _ok(
            "guardrails_module",
            (root / "nz_startup" / "agent_guardrails.py").is_file(),
            "nz_startup/agent_guardrails.py",
        )
    )
    checks.append(
        _ok(
            "hitl_module",
            (root / "nz_startup" / "hitl.py").is_file(),
            "nz_startup/hitl.py",
        )
    )
    harden_skill = skills_dir() / "agent-hardening" / "SKILL.md"
    checks.append(
        _ok("skill_agent_hardening", harden_skill.is_file(), str(harden_skill))
    )

    # MCP inventory must not include forbidden names
    try:
        from nz_startup.mcp_server import tool_inventory

        inv = set(tool_inventory())
        overlap = inv & FORBIDDEN_TOOL_NAMES
        checks.append(
            _ok(
                "mcp_no_forbidden_tools",
                len(overlap) == 0,
                "clean" if not overlap else f"forbidden present: {sorted(overlap)}",
            )
        )
    except Exception as e:  # noqa: BLE001
        checks.append(_ok("mcp_no_forbidden_tools", False, f"inventory error: {e}"))

    # Forbidden tools list non-empty (policy loaded)
    checks.append(
        _ok(
            "hitl_policy_loaded",
            len(FORBIDDEN_TOOL_NAMES) >= 15,
            f"{len(FORBIDDEN_TOOL_NAMES)} forbidden tool names",
        )
    )

    # Autonomy slogan present in COMPLIANCE
    comp = (root / "COMPLIANCE.md").read_text(encoding="utf-8", errors="replace")
    checks.append(
        _ok(
            "autonomy_in_compliance_doc",
            "Inform, draft, prepare, monitor, remind" in comp
            or "inform, draft, prepare, monitor, remind" in comp.lower(),
            "COMPLIANCE.md states autonomy ceiling",
        )
    )

    # Optional company checks
    if company_id:
        cdir = company_dir(company_id)
        checks.append(
            _ok(
                "company_exists",
                cdir.is_dir(),
                str(cdir),
            )
        )
        audit = cdir / "audit.jsonl"
        checks.append(
            _ok(
                "company_audit_log",
                audit.is_file(),
                str(audit),
                severity="soft",
            )
        )
        # scan for obvious secret filenames
        bad_names = []
        if cdir.is_dir():
            for p in cdir.rglob("*"):
                if p.is_file():
                    n = p.name.lower()
                    if any(x in n for x in (".pem", "id_rsa", ".env", "service_role")):
                        bad_names.append(str(p.relative_to(cdir)))
        checks.append(
            _ok(
                "company_no_secret_filenames",
                len(bad_names) == 0,
                "clean" if not bad_names else f"suspicious: {bad_names[:5]}",
            )
        )

    hard_fail = [c for c in checks if not c["passed"] and c.get("severity") == "hard"]
    soft_fail = [c for c in checks if not c["passed"] and c.get("severity") == "soft"]

    return {
        "ok": len(hard_fail) == 0,
        "product_version": __version__,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "licence": "proprietary",
        "company_id": company_id,
        "checks": checks,
        "hard_failures": [c["name"] for c in hard_fail],
        "soft_failures": [c["name"] for c in soft_fail],
        "disclaimer": (
            "This gate validates product control presence. "
            "It is NOT a legal compliance certificate for your business."
        ),
    }


def format_compliance_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Compliance gate — v{report.get('product_version')}",
        "",
        f"- Overall: **{'PASS' if report.get('ok') else 'FAIL'}**",
        f"- Licence posture: **{report.get('licence')}**",
        f"- Generated: {report.get('generated_at')}",
        "",
        report.get("disclaimer", ""),
        "",
        "## Checks",
        "",
    ]
    for c in report.get("checks") or []:
        mark = "OK" if c.get("passed") else ("SOFT" if c.get("severity") == "soft" else "FAIL")
        lines.append(f"- [{mark}] **{c.get('name')}** — {c.get('detail')}")
    if report.get("hard_failures"):
        lines.extend(["", "## Hard failures", ""])
        for n in report["hard_failures"]:
            lines.append(f"- {n}")
    lines.append("")
    return "\n".join(lines)


def write_compliance_report(company_id: str | None = None) -> tuple[dict[str, Any], Path]:
    report = run_compliance_check(company_id)
    out_dir = repo_root() / "compliance" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"compliance-gate-{stamp}.md"
    latest = out_dir / "compliance-gate-latest.md"
    md = format_compliance_markdown(report)
    path.write_text(md, encoding="utf-8", newline="\n")
    latest.write_text(md, encoding="utf-8", newline="\n")
    (out_dir / "compliance-gate-latest.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report, latest
