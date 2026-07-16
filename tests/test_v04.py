"""v0.4 Xero read-only + reminder export tests."""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from nz_startup import calendar_ops, export_reminders, memory, xero_readonly
from nz_startup.hitl import check_action
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory


@pytest.fixture()
def company(tmp_path, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
 monkeypatch.delenv("XERO_ACCESS_TOKEN", raising=False)
 monkeypatch.delenv("XERO_TENANT_ID", raising=False)
 src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
 dest_root = tmp_path / "memory"
 (dest_root / "companies").mkdir(parents=True)
 import shutil

 shutil.copytree(src, dest_root / "example-company")
 cid = "v4co"
 memory.init_company(cid)
 return cid


def test_xero_offline_snapshot(company):
 snap = xero_readonly.fetch_snapshot(company, force_offline=True)
 assert snap["mode"] == "offline"
 paths = xero_readonly.write_snapshot(company, snap)
 assert paths["json"].is_file()
 assert paths["markdown"].is_file()
 text = paths["markdown"].read_text(encoding="utf-8")
 assert "read-only" in text.lower() or "Read-only" in text
 assert "token" not in text.lower() or "Never" in text


def test_xero_status_no_secrets():
 st = xero_readonly.credentials_status()
 assert st["mode"] in ("offline", "live")
 blob = str(st)
 assert "eyJ" not in blob # no JWT-looking token


def test_hitl_blocks_xero_write_and_email_digest():
 assert check_action("create payment in xero").allowed is False
 assert check_action("email digest to founder").allowed is False


def test_ics_export_contains_vevent(company):
 due = (date.today() + timedelta(days=5)).isoformat()
 calendar_ops.add_item(company, item="Board pack due", due=due, category="board")
 ics = export_reminders.build_ics(company, within_days=30)
 assert "BEGIN:VCALENDAR" in ics
 assert "BEGIN:VEVENT" in ics
 assert "Board pack due" in ics


def test_export_all_writes_files(company):
 due = (date.today() + timedelta(days=2)).isoformat()
 calendar_ops.add_item(company, item="Pilot export", due=due, category="ops")
 paths = export_reminders.export_all(company, within_days=14, ics_days=60)
 assert paths["ics"].is_file()
 assert paths["digest"].is_file()
 assert paths["ics_latest"].is_file()
 digest = paths["digest"].read_text(encoding="utf-8")
 assert "does not send" in digest.lower() or "Export only" in digest


def test_mcp_v4_tools():
 inv = tool_inventory()
 assert "xero_snapshot" in inv
 assert "export_deadline_reminders" in inv
 assert "create_payment" not in inv
 assert_no_forbidden_tools()
