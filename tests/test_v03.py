"""v0.3 pipeline, calendar, grants tests."""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from nz_startup import calendar_ops, grants, memory, pipeline
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory


@pytest.fixture()
def company(tmp_path, monkeypatch):
    monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
    monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
    src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
    dest_root = tmp_path / "memory"
    (dest_root / "companies").mkdir(parents=True)
    import shutil

    shutil.copytree(src, dest_root / "example-company")
    cid = "v3co"
    memory.init_company(cid)
    return cid


def test_pipeline_add_update_summary(company):
    row = pipeline.add_deal(
        company,
        account="Taranaki Regional Council",
        stage="discovery",
        next_step="book site demo",
        value_nzd="1500",
    )
    assert row["id"].startswith("P")
    updated = pipeline.update_deal(company, row["id"], stage="pilot", next_step="LOI")
    assert updated["stage"] == "pilot"
    md = pipeline.format_summary_markdown(company)
    assert "Taranaki Regional Council" in md
    assert "pilot" in md


def test_pipeline_rejects_bad_stage(company):
    with pytest.raises(ValueError):
        pipeline.add_deal(company, account="X", stage="teleport")


def test_calendar_reminders(company):
    soon = (date.today() + timedelta(days=3)).isoformat()
    past = (date.today() - timedelta(days=2)).isoformat()
    calendar_ops.add_item(company, item="GST worksheet prep", due=soon, category="finance")
    calendar_ops.add_item(company, item="Annual return prep", due=past, category="compliance")
    data = calendar_ops.reminders(company, within_days=14)
    assert data["count_actionable"] >= 2
    assert any(r["item"] == "Annual return prep" for r in data["overdue"])
    assert any(r["item"] == "GST worksheet prep" for r in data["upcoming"])
    md = calendar_ops.format_reminders_markdown(company)
    assert "Deadline reminders" in md


def test_grants_rank(company):
    # seed already added RDTI etc on init
    grants.add_grant(
        company,
        name="Test Sector Fund",
        funder="Example",
        status="open",
        fit_score="90",
        next_action="draft EOI",
    )
    ranked = grants.rank_by_fit(company, min_score=50)
    assert ranked
    assert int(ranked[0]["fit_score"]) >= int(ranked[-1]["fit_score"])


def test_init_seeds_trackers(company):
    assert pipeline.list_deals(company)
    assert calendar_ops.list_items(company)
    assert grants.list_grants(company)


def test_mcp_inventory_has_v3_tools():
    inv = tool_inventory()
    for name in (
        "pipeline_add",
        "pipeline_update",
        "calendar_reminders",
        "grants_rank",
    ):
        assert name in inv
    assert_no_forbidden_tools()
