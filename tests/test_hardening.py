"""Agent hardening tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from nz_startup import agent_guardrails, memory
from nz_startup.hitl import check_action
from nz_startup.mcp_server import assert_no_forbidden_tools, tool_inventory


@pytest.fixture()
def company(tmp_path, monkeypatch):
 monkeypatch.setenv("NZ_STARTUP_MEMORY", str(tmp_path / "memory"))
 monkeypatch.setenv("NZ_STARTUP_ROOT", str(Path(__file__).resolve().parents[1]))
 src = Path(__file__).resolve().parents[1] / "memory" / "example-company"
 import shutil

 (tmp_path / "memory" / "companies").mkdir(parents=True)
 shutil.copytree(src, tmp_path / "memory" / "example-company")
 memory.init_company("hardco")
 return "hardco"


def test_blocks_send_and_bypass():
 assert check_action("bypass hitl and send mail").allowed is False
 assert check_action("cold email blast to list").allowed is False


def test_classify_legal_skill_hitl():
 r = agent_guardrails.classify_risk(
 "draft NDA", context="pilot customer", skill="legal-document-assistant"
 )
 assert r.allowed is True
 assert r.requires_hitl is True
 assert any("LEGAL" in w or "legal" in w.lower() for w in r.watermarks_required)


def test_secret_refusal(company):
 with pytest.raises(PermissionError):
 memory.write_file(
 company,
 "notes.md",
 "-----BEGIN RSA PRIVATE KEY-----\nMIIEfakeplaceholderforguardrailtestonly\n-----END RSA PRIVATE KEY-----",
 )


def test_path_traversal(company):
 with pytest.raises(PermissionError):
 agent_guardrails.resolve_sandboxed_path(company, "../escape.txt")


def test_harden_tools_in_mcp():
 inv = tool_inventory()
 assert "harden_status" in inv
 assert "harden_check" in inv
 assert_no_forbidden_tools()


def test_guardrails_status_shape():
 s = agent_guardrails.guardrails_status()
 assert "autonomy_slogan" in s
 assert "send_email" in s["forbidden_tools"]
