"""v0.8 status, board pack, smoke tests."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from nz_startup import board_pack, memory, pipeline, status
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory


@pytest.fixture()
def company(tmp_path, monkeypatch):
    monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
    monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
    src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
    dest = tmp_path / "memory"
    (dest / "companies").mkdir(parents=True)
    import shutil

    shutil.copytree(src, dest / "example-company")
    cid = "v8co"
    memory.init_company(cid)
    pipeline.add_deal(cid, account="Mentor Co", stage="discovery", next_step="call")
    return cid


def test_status_score(company):
    st, path = status.write_status(company)
    assert 0 <= st["score"] <= 100
    assert st["band"] in {"early", "progressing", "ready"}
    assert path.is_file()
    md = status.format_status_markdown(st)
    assert "Company status" in md


def test_board_pack(company):
    result = board_pack.create_board_pack(company, label="test")
    z = Path(result["zip"])
    assert z.is_file()
    with ZipFile(z) as zf:
        names = zf.namelist()
        assert "BOARD_README.md" in names
        assert any("status" in n or "pipeline" in n or "weekly" in n for n in names)


def test_mcp_v8_tools():
    inv = tool_inventory()
    assert "company_status" in inv
    assert "board_pack_create" in inv
    assert "smoke_run" in inv
    assert_no_forbidden_tools()
