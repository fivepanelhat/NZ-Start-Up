"""v0.5 bank feed + GST worksheet tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from nz_startup import bank_feed, gst_worksheet, memory, xero_readonly
from nz_startup.hitl import check_action
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory
from nz_startup.paths import repo_root


@pytest.fixture()
def company(tmp_path, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
 src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
 dest_root = tmp_path / "memory"
 (dest_root / "companies").mkdir(parents=True)
 import shutil

 shutil.copytree(src, dest_root / "example-company")
 cid = "v5co"
 memory.init_company(cid)
 return cid


def test_bank_import_sample(company):
 sample = repo_root() / "templates" / "bank-feed-sample.csv"
 summary = bank_feed.import_csv(company, sample)
 assert summary["added"] >= 5
 rows = bank_feed.list_transactions(company)
 assert any("AWS" in (r.get("description") or "") for r in rows)
 triage = bank_feed.triage_summary(company)
 assert triage["total_rows"] == summary["total_rows"]
 assert triage["inflow_sum"] > 0


def test_bank_duplicate_skip(company):
 sample = repo_root() / "templates" / "bank-feed-sample.csv"
 bank_feed.import_csv(company, sample)
 second = bank_feed.import_csv(company, sample)
 assert second["added"] == 0
 assert second["skipped_duplicates"] > 0


def test_gst_worksheet(company):
 sample = repo_root() / "templates" / "bank-feed-sample.csv"
 bank_feed.import_csv(company, sample)
 xero_readonly.write_snapshot(
 company, xero_readonly.fetch_snapshot(company, force_offline=True)
 )
 ws, paths = gst_worksheet.prepare_and_write(
 company,
 period_start="2026-07-01",
 period_end="2026-07-31",
 )
 assert ws["not_a_tax_filing"] is True
 assert paths["markdown"].is_file()
 assert paths["lines_csv"].is_file()
 md = paths["markdown"].read_text(encoding="utf-8")
 assert "NOT A TAX FILING" in md
 assert "Net GST" in md


def test_hitl_blocks_file_gst():
 assert check_action("file gst return in myIR").allowed is False
 assert check_action("bank transfer to supplier").allowed is False


def test_mcp_v5_tools():
 inv = tool_inventory()
 assert "bank_import_csv" in inv
 assert "gst_prepare_worksheet" in inv
 assert "file_gst_return" not in inv
 assert_no_forbidden_tools()
