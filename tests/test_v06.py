"""v0.6 invoice triage + accountant handoff pack tests."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from nz_startup import bank_feed, handoff, invoice_triage, memory, xero_readonly
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
    cid = "v6co"
    memory.init_company(cid)
    return cid


def test_parse_sample_invoice_text():
    sample = (repo_root() / "templates" / "sample-tax-invoice.txt").read_text(
        encoding="utf-8"
    )
    parsed = invoice_triage.parse_invoice_text(sample)
    assert parsed["invoice_number"] == "CT-1042"
    assert parsed["total"] == "345.00"
    assert parsed["gst"] == "45.00"
    assert "123" in (parsed.get("gst_number_guess") or "")
    assert parsed["confidence"] in {"medium", "high"}


def test_triage_file_writes_registry(company):
    sample = repo_root() / "templates" / "sample-tax-invoice.txt"
    detail = invoice_triage.triage_file(company, sample)
    assert detail["id"].startswith("I")
    rows = invoice_triage.list_invoices(company)
    assert any(r.get("invoice_number") == "CT-1042" for r in rows)
    summary = invoice_triage.format_registry_summary(company)
    assert "CT-1042" in summary or "Cloud" in summary


def test_handoff_pack_zip(company):
    sample_bank = repo_root() / "templates" / "bank-feed-sample.csv"
    bank_feed.import_csv(company, sample_bank)
    xero_readonly.write_snapshot(
        company, xero_readonly.fetch_snapshot(company, force_offline=True)
    )
    inv = repo_root() / "templates" / "sample-tax-invoice.txt"
    invoice_triage.triage_file(company, inv)
    result = handoff.create_handoff_pack(company, label="test")
    zpath = Path(result["zip"])
    assert zpath.is_file()
    with ZipFile(zpath) as zf:
        names = zf.namelist()
        assert "HANDOFF_README.md" in names
        assert "manifest.json" in names
        assert any("bank-feed" in n for n in names)


def test_hitl_blocks_email_handoff_and_claim():
    assert check_action("email handoff pack to accountant").allowed is False
    assert check_action("claim gst automatically").allowed is False


def test_mcp_v6_tools():
    inv = tool_inventory()
    assert "invoice_triage_path" in inv
    assert "handoff_pack_create" in inv
    assert "email_handoff" not in inv
    assert_no_forbidden_tools()
