"""v1.8 market-fit + investor readiness tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from nz_startup import market_fit, memory


def test_matrix_ranks_eda_first():
 rows = market_fit.matrix_table()
 assert rows[0]["id"] == "S2"
 assert rows[0]["total"] >= 26


def test_score_segment_s1():
 r = market_fit.score_segment("S1")
 assert r["total"] == 26
 assert "GO" in r["decision"]


def test_unknown_segment():
 with pytest.raises(ValueError):
 market_fit.score_segment("S99")


def test_enterprise_products_present():
 assert len(market_fit.ENTERPRISE_PRODUCTS) >= 7
 ids = {p["id"] for p in market_fit.ENTERPRISE_PRODUCTS}
 assert "A" in ids and "C" in ids


def test_portfolio_includes_nz_startup():
 repos = {p["repo"] for p in market_fit.PORTFOLIO}
 assert "NZ-Start-Up" in repos
 lead = next(p for p in market_fit.PORTFOLIO if p["repo"] == "NZ-Start-Up")
 assert lead["total"] == 25


def test_markdown_formatters():
 assert "S2" in market_fit.format_matrix_markdown()
 assert "EDA fleet" in market_fit.format_enterprise_markdown() or "EDA" in market_fit.format_enterprise_markdown()
 assert "NZ-Start-Up" in market_fit.format_portfolio_markdown()


def test_skills_exist():
 root = Path(__file__).resolve().parents[1] / "skills"
 assert (root / "enterprise-adoption-officer" / "SKILL.md").is_file()
 assert (root / "investor-readiness-clerk" / "SKILL.md").is_file()


def test_docs_exist():
 root = Path(__file__).resolve().parents[1] / "docs"
 for name in (
 "MARKET_FIT_MATRIX.md",
 "PORTFOLIO_MARKET_FIT.md",
 "SEED_INVESTOR_PACK.md",
 ):
 assert (root / name).is_file()


@pytest.fixture()
def company(tmp_path, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
 src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
 import shutil

 (tmp_path / "memory" / "companies").mkdir(parents=True)
 shutil.copytree(src, tmp_path / "memory" / "example-company")
 memory.init_company("seedco")
 return "seedco"


def test_investor_data_room_cli(company, monkeypatch):
 from nz_startup.cli import main
 import sys

 monkeypatch.setattr(
 sys,
 "argv",
 ["nz-startup", "investor", "data-room", company],
 )
 try:
 main()
 except SystemExit as e:
 assert e.code == 0
 path = memory.ensure_exists(company) / "commercial" / "data-room-index.md"
 assert path.is_file()
 text = path.read_text(encoding="utf-8")
 assert "SEED_INVESTOR_PACK" in text
 assert "NEEDS_EVIDENCE" in text
