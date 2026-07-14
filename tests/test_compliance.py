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
    assert "DUAL" in text.upper() or "Track A" in text


def test_dual_commercial_track_exists():
    text = (repo_root() / "LICENSE-COMMERCIAL.md").read_text(encoding="utf-8")
    assert "Track B" in text
    assert "Commercial" in text


def test_notice_proprietary():
    text = (repo_root() / "NOTICE").read_text(encoding="utf-8")
    assert "PROPRIETARY" in text.upper()
    assert "Pre-seed" in text or "PRE-SEED" in text.upper()
    assert "Wayne Roberts" in text
    assert "8 August 2025" in text
    assert "8 August 2026" in text


def test_about_preseed():
    text = (repo_root() / "ABOUT.md").read_text(encoding="utf-8")
    assert "six generations" in text.lower() or "6 generations" in text
    assert "Taranaki" in text


def test_readme_badges():
    text = (repo_root() / "README.md").read_text(encoding="utf-8")
    for needle in (
        "Grok%204.5",
        "Claude%20Pro",
        "Computer%20Use",
        "Gemini",
        "Pre--seed",
        "Dual",
    ):
        assert needle in text or needle.replace("%20", " ") in text


def test_compliance_gate_pass():
    report = compliance_gate.run_compliance_check(None)
    assert report["ok"] is True, report.get("hard_failures")
    assert "dual" in report["licence"] or "proprietary" in report["licence"]
    md = compliance_gate.format_compliance_markdown(report)
    assert "PASS" in md


def test_compliance_mcp_tool():
    assert "compliance_check" in tool_inventory()


def test_pyproject_not_apache():
    text = (repo_root() / "pyproject.toml").read_text(encoding="utf-8")
    assert "Apache-2.0" not in text
    assert "Proprietary" in text or "LicenseRef-Coastal" in text
