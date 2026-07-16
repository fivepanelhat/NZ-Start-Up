"""Tests for first-principles operator brief."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from nz_startup import memory, operator, pipeline


@pytest.fixture()
def company(tmp_path, monkeypatch):
    monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
    monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
    src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
    dest_root = tmp_path / "memory"
    (dest_root / "companies").mkdir(parents=True)
    shutil.copytree(src, dest_root / "example-company")
    cid = "op-test"
    memory.init_company(cid, force=True)
    return cid


def test_operate_brief_writes_and_ranks(company):
    pipeline.add_deal(company, account="Acme Co", stage="lead", next_step="")
    path, state = operator.write_operator_brief(company)
    assert path.is_file()
    assert state["priorities"]
    md = path.read_text(encoding="utf-8")
    assert "Operator brief" in md
    assert path.parent.joinpath("brief-latest.md").is_file()


def test_cli_operate(company):
    from nz_startup.cli import build_parser

    p = build_parser()
    args = p.parse_args(["operate", company])
    assert args.func is not None
    rc = args.func(args)
    assert rc == 0
