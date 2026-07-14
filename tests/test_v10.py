"""v1.0 doctor + console tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from nz_startup import console, doctor, memory
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory


@pytest.fixture()
def env(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    mem = root / "memory"
    monkeypatch.setenv("NZ_STARTUP_ROOT", str(root))
    monkeypatch.setenv("NZ_STARTUP_MEMORY", str(mem))
    real = Path(__file__).resolve().parents[1]
    import shutil

    shutil.copytree(real / "templates", root / "templates")
    shutil.copytree(real / "memory" / "example-company", mem / "example-company")
    (mem / "companies").mkdir(parents=True)
    # minimal skills so doctor can count
    for name in (
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
    ):
        d = root / "skills" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: t\nversion: \"0.1.0\"\n---\n# t\n",
            encoding="utf-8",
        )
    (root / "scripts").mkdir(exist_ok=True)
    (root / "scripts" / "validate_skills.py").write_text("# stub\n", encoding="utf-8")
    return root


def test_doctor_pass(env):
    report = doctor.run_doctor()
    assert report["ok"] is True
    md = doctor.format_doctor_markdown(report)
    assert "PASS" in md or "Doctor" in md


def test_console_refuses_nonlocal_bind():
    with pytest.raises(ValueError, match="localhost"):
        console.run_console(host="0.0.0.0", port=8765)


def test_console_pages(env):
    memory.init_company("conco")
    html = console.page_home()
    assert "Founder companies" in html
    html2 = console.page_company("conco")
    assert "conco" in html2
    assert "100" in html2 or "score" in html2.lower() or "/100" in html2
    assert "Pipeline" in html2
    assert "Board pack" in html2 or "board" in html2.lower()


def test_mcp_v10_tools():
    inv = tool_inventory()
    assert "doctor_run" in inv
    assert_no_forbidden_tools()
