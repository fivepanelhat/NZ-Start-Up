"""Compliance gate + proprietary licence tests."""
from __future__ import annotations

from pathlib import Path

from nz_startup import compliance_gate
from nz_startup.mcp_server import tool_inventory
from nz_startup.paths import repo_root


def test_licence_is_proprietary():
    text = (repo_root() / "LICENSE").read_text(encoding="utf-8")
    assert "PROPRIETARY" in text.upper()
    assert "Apache License" not in text
    assert "Coastal Alpine Tech" in text


def test_notice_proprietary():
    text = (repo_root() / "NOTICE").read_text(encoding="utf-8")
    assert "PROPRIETARY" in text.upper()


def test_compliance_gate_pass():
    report = compliance_gate.run_compliance_check(None)
    assert report["ok"] is True, report.get("hard_failures")
    assert report["licence"] == "proprietary"
    md = compliance_gate.format_compliance_markdown(report)
    assert "PASS" in md


def test_compliance_mcp_tool():
    assert "compliance_check" in tool_inventory()


def test_pyproject_not_apache():
    text = (repo_root() / "pyproject.toml").read_text(encoding="utf-8")
    assert "Apache-2.0" not in text
    assert "Proprietary" in text or "LicenseRef-Coastal" in text
