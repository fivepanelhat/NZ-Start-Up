"""Runtime / CLI / HITL tests for v0.2."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from nz_startup import drafts, hitl, memory, nzbn, rdti, weekly
from nz_startup.hitl import FORBIDDEN_TOOL_NAMES, check_action
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory
from nz_startup.paths import companies_dir


@pytest.fixture()
def company(tmp_path, monkeypatch):
 # Point memory at temp
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
 # seed example into temp memory layout
 src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
 dest_root = tmp_path / "memory"
 (dest_root / "companies").mkdir(parents=True)
 import shutil

 shutil.copytree(src, dest_root / "example-company")
 cid = "test-co"
 memory.init_company(cid)
 return cid


def test_hitl_blocks_send():
 d = check_action("send_email to prospect")
 assert d.allowed is False
 assert d.requires_human is True


def test_hitl_allows_draft():
 d = check_action("save outreach draft")
 assert d.allowed is True


def test_forbidden_tools_not_in_inventory():
 assert_no_forbidden_tools()
 inv = set(tool_inventory())
 assert inv.isdisjoint(FORBIDDEN_TOOL_NAMES)
 assert "send_email" not in inv


def test_rdti_append_and_list(company):
 row = rdti.append_entry(
 company,
 hours=1.5,
 activity="Offline inference latency experiment",
 technical_uncertainty="Whether quantised model meets SLA offline",
 evidence_ref="commit:deadbeef",
 )
 assert float(row["hours"]) == 1.5
 rows = rdti.list_entries(company)
 assert any(r.get("evidence_ref") == "commit:deadbeef" for r in rows)


def test_rdti_rejects_invented_hours(company):
 with pytest.raises(ValueError):
 rdti.append_entry(
 company,
 hours=0,
 activity="x",
 technical_uncertainty="y",
 evidence_ref="z",
 )


def test_outreach_draft_watermark(company):
 path = drafts.save_outreach_draft(
 company,
 subject="Intro",
 body="Hello",
 to_hint="founder@example.com",
 )
 text = path.read_text(encoding="utf-8")
 assert "DRAFT_NOT_SENT" in text
 assert "UEM Act" in text


def test_weekly_review(company):
 path = weekly.generate_weekly_review(company)
 assert path.is_file()
 text = path.read_text(encoding="utf-8")
 assert "Weekly" in text or "Operating" in text


def test_nzbn_offline_no_key(monkeypatch):
 monkeypatch.delenv("BUSINESS_GOVT_API_KEY", raising=False)
 monkeypatch.delenv("NZBN_API_KEY", raising=False)
 result = nzbn.lookup_entities("Coastal Alpine")
 assert result["mode"] == "offline"
 assert result["entities"] == []
 md = nzbn.format_lookup_markdown(result)
 assert "NOT FOR SUBMISSION" in md


def test_write_refuses_secret_path(company):
 with pytest.raises(PermissionError):
 memory.write_file(company, "secrets/password.txt", "x")


def test_cli_help():
 from nz_startup.cli import build_parser

 p = build_parser()
 assert p.parse_args(["list"]).command == "list"
