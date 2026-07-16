"""v0.9 onboard, pilot offer, partner report tests."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from nz_startup import cohort, onboard, partner_report, pilot_offer
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
 (root / "skills" / "x").mkdir(parents=True)
 (root / "skills" / "x" / "SKILL.md").write_text(
 "---\nname: x\ndescription: t\nversion: \"0.1.0\"\n---\n# t\n",
 encoding="utf-8",
 )
 return root


def test_onboard(env):
 result = onboard.run_onboard(
 "freshco",
 legal_name="Fresh Co Limited",
 wedge="Local AI for operators",
 icp="Regional councils",
 )
 assert result["company_id"] == "freshco"
 assert Path(result["paths"]["plan_30_day"]).is_file()
 assert result["score"] is not None


def test_pilot_offer(env):
 onboard.run_onboard("pilotco", legal_name="Pilot Co")
 offer, paths = pilot_offer.prepare_and_write(
 "pilotco",
 customer_name="Taranaki Example Ltd",
 pilot_fee_nzd="1500",
 term_days=90,
 champion="Alex",
 )
 assert offer["status"] == "DRAFT_NOT_SENT"
 assert Path(paths["zip"]).is_file()
 with ZipFile(paths["zip"]) as zf:
 assert "PILOT_OFFER.md" in zf.namelist()
 md = pilot_offer.format_offer_markdown(offer)
 assert "DRAFT_NOT_SENT" in md


def test_partner_report(env):
 cohort.init_cohort(
 "eda1",
 partner_name="Test EDA",
 programme="Demo",
 seat_quota=5,
 force=True,
 )
 cohort.add_seat("eda1", founder_id="f1", company_id="seat1")
 onboard.run_onboard("seat1", force=True)
 report, path = partner_report.write_partner_report("eda1", anonymise=True)
 assert report["anonymised"] is True
 assert report["seats_active"] == 1
 assert path.is_file()
 assert "seat-01" in path.read_text(encoding="utf-8")


def test_mcp_v9_tools():
 inv = tool_inventory()
 assert "onboard_company" in inv
 assert "pilot_offer_create" in inv
 assert "cohort_partner_report" in inv
 assert_no_forbidden_tools()
