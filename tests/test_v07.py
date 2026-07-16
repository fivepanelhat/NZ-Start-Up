"""v0.7 cohort white-label + demo walkthrough tests."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from nz_startup import cohort, demo
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory
from nz_startup.paths import repo_root


@pytest.fixture()
def env(tmp_path, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(tmp_path / "repo"))
 # minimal repo layout for cohort + demo
 root = tmp_path / "repo"
 (root / "skills" / "board-chief-of-staff").mkdir(parents=True)
 (root / "skills" / "board-chief-of-staff" / "SKILL.md").write_text(
 "---\nname: board-chief-of-staff\ndescription: test\nversion: \"0.1.0\"\n---\n# t\n",
 encoding="utf-8",
 )
 # copy templates needed by demo from real repo
 real = Path(__file__).resolve().parents[1]
 import shutil

 shutil.copytree(real / "templates", root / "templates")
 shutil.copytree(real / "memory" / "example-company", root / "memory" / "example-company")
 (root / "memory" / "companies").mkdir(parents=True, exist_ok=True)
 return root


def test_cohort_init_seat_pack(env, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(env))
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(env / "memory"))
 cfg = cohort.init_cohort(
 "vt-powerup",
 partner_name="Venture Taranaki",
 programme="PowerUp",
 seat_quota=5,
 )
 assert cfg["cohort_id"] == "vt-powerup"
 seat = cohort.add_seat(
 "vt-powerup",
 founder_id="alice",
 company_id="alice-co",
 display_name="Alice",
 )
 assert seat["company_id"] == "alice-co"
 assert len(cohort.list_seats("vt-powerup")) == 1
 md = cohort.format_cohort_markdown("vt-powerup")
 assert "Venture Taranaki" in md
 pack = cohort.build_white_label_pack("vt-powerup")
 z = Path(pack["zip"])
 assert z.is_file()
 with ZipFile(z) as zf:
 names = zf.namelist()
 assert "README.md" in names
 assert "cohort.json" in names
 # seats must not be in distribution pack
 raw = zf.read("cohort.json").decode("utf-8")
 assert "alice" not in raw


def test_demo_quick(env, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(env))
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(env / "memory"))
 report = demo.run_demo(
 "demo-quick",
 partner="Venture Taranaki",
 quick=True,
 )
 assert report["partner"] == "Venture Taranaki"
 assert any(s["step"] == "weekly_board" and s["ok"] for s in report["steps"])
 latest = Path(report["paths"]["latest_md"])
 assert latest.is_file()
 text = latest.read_text(encoding="utf-8")
 assert "did **not** send email" in text or "did not" in text.lower()


def test_mcp_v7_tools():
 inv = tool_inventory()
 assert "cohort_pack" in inv
 assert "demo_run" in inv
 assert_no_forbidden_tools()
