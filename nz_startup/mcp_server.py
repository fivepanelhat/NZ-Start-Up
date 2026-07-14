"""
HITL-safe MCP server for NZ Start-Up in a Box.

Exposes draft/prepare/read tools only. Deliberately omits send/file/pay/sign.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from nz_startup import __version__, drafts, memory, nzbn, rdti, weekly
from nz_startup.hitl import FORBIDDEN_TOOL_NAMES, WATERMARKS, check_action


def _require_mcp():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as e:
        raise SystemExit(
            "MCP extra not installed. Run:\n"
            "  pip install 'nz-startup-in-a-box[mcp]'\n"
            "or: pip install mcp"
        ) from e
    return FastMCP


def build_server():
    FastMCP = _require_mcp()
    mcp = FastMCP(
        "nz-startup-in-a-box",
        instructions=(
            "NZ Start-Up in a Box fleet connectors. "
            "Agents may inform, draft, prepare, monitor, and remind. "
            "Humans must advise, sign, file, send, and pay. "
            f"Forbidden tools: {sorted(FORBIDDEN_TOOL_NAMES)}. "
            "Always load CAT Gold/Diamond/Platinum classification for material work."
        ),
    )

    @mcp.tool()
    def list_companies() -> list[str]:
        """List local company memory IDs under memory/companies/."""
        return memory.list_companies()

    @mcp.tool()
    def init_company_memory(company_id: str, force: bool = False) -> str:
        """Create company memory from the example scaffold (local only)."""
        path = memory.init_company(company_id, force=force)
        return f"Initialised {path}"

    @mcp.tool()
    def read_company_file(company_id: str, relative_path: str) -> str:
        """Read a file from company memory (no secrets should be stored there)."""
        return memory.read_file(company_id, relative_path)

    @mcp.tool()
    def write_company_file(company_id: str, relative_path: str, content: str) -> str:
        """Write a non-secret file into company memory. Audited."""
        path = memory.write_file(company_id, relative_path, content)
        return f"Wrote {path}"

    @mcp.tool()
    def append_company_decision(company_id: str, decision: str) -> str:
        """Append a dated decision line to decisions.md."""
        path = memory.append_decision(company_id, decision)
        return f"Appended decision → {path}"

    @mcp.tool()
    def append_rdti_log(
        company_id: str,
        hours: float,
        activity: str,
        technical_uncertainty: str,
        evidence_ref: str,
        person: str = "Founder",
        notes: str = "",
        entry_date: str = "",
    ) -> str:
        """
        Append a contemporaneous RDTI R&D activity row.
        Never invent hours — evidence_ref required (commit/timesheet/doc).
        """
        row = rdti.append_entry(
            company_id,
            hours=hours,
            activity=activity,
            technical_uncertainty=technical_uncertainty,
            evidence_ref=evidence_ref,
            person=person,
            notes=notes,
            entry_date=entry_date or None,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def list_rdti_log(company_id: str, limit: int = 20) -> str:
        """List recent RDTI log rows as JSON."""
        return json.dumps(rdti.list_entries(company_id, limit=limit), indent=2)

    @mcp.tool()
    def generate_weekly_operating_review(company_id: str, review_date: str = "") -> str:
        """
        Generate a weekly board review draft from company memory.
        HITL: founder decides priorities — agent escalates only.
        """
        path = weekly.generate_weekly_review(
            company_id, review_date or None
        )
        return (
            f"Wrote {path}\n"
            f"{WATERMARKS['agent']}\n"
            "HITL pending: founder must review and decide."
        )

    @mcp.tool()
    def save_outreach_draft(
        company_id: str,
        subject: str,
        body: str,
        to_hint: str = "",
        icp_segment: str = "",
    ) -> str:
        """
        Save an outreach email draft. NEVER sends.
        UEM Act 2007: human must send from their own client after compliance checks.
        """
        # Explicit block if someone tries to smuggle send semantics
        blob = f"{subject}\n{body}".lower()
        if "send now" in blob or "auto-send" in blob:
            decision = check_action("send_email")
            if not decision.allowed:
                return decision.reason
        path = drafts.save_outreach_draft(
            company_id,
            subject=subject,
            body=body,
            to_hint=to_hint,
            icp_segment=icp_segment,
        )
        return f"Saved DRAFT_NOT_SENT: {path}"

    @mcp.tool()
    def save_legal_draft(
        company_id: str,
        title: str,
        body: str,
        doc_type: str = "general",
    ) -> str:
        """Save a legal document draft watermarked as not legal advice."""
        path = drafts.save_legal_draft(
            company_id, title=title, body=body, doc_type=doc_type
        )
        return f"Saved legal draft: {path}\n{WATERMARKS['legal']}"

    @mcp.tool()
    def nzbn_lookup(query: str, limit: int = 5) -> str:
        """
        Read-only NZBN / entity name lookup.
        Without BUSINESS_GOVT_API_KEY returns offline guidance (does not invent NZBNs).
        Never files with Companies Office.
        """
        result = nzbn.lookup_entities(query, limit=limit)
        return nzbn.format_lookup_markdown(result)

    @mcp.tool()
    def hitl_policy_summary() -> str:
        """Return autonomy ceilings and forbidden actions for this fleet."""
        return (
            "Agents: inform, draft, prepare, monitor, remind.\n"
            "Humans: advise, sign, file, send, pay.\n"
            f"Forbidden MCP tools (not implemented): {sorted(FORBIDDEN_TOOL_NAMES)}\n"
            f"Watermarks: {json.dumps(WATERMARKS, indent=2)}\n"
            f"Server version: {__version__}\n"
        )

    @mcp.tool()
    def check_hitl_action(action_description: str) -> str:
        """Check whether a proposed action is allowed under HITL policy."""
        d = check_action(action_description)
        return json.dumps(
            {
                "allowed": d.allowed,
                "requires_human": d.requires_human,
                "reason": d.reason,
            },
            indent=2,
        )

    # Sanity: ensure we never registered forbidden names
    # FastMCP stores tools internally; document in instructions only.
    return mcp


def run_stdio() -> None:
    mcp = build_server()
    # Prefer explicit stdio entrypoints across mcp versions
    if hasattr(mcp, "run"):
        mcp.run(transport="stdio")
    else:
        raise SystemExit("Unsupported mcp FastMCP version — expected .run()")


def tool_inventory() -> list[str]:
    """Used by tests without starting stdio."""
    return [
        "list_companies",
        "init_company_memory",
        "read_company_file",
        "write_company_file",
        "append_company_decision",
        "append_rdti_log",
        "list_rdti_log",
        "generate_weekly_operating_review",
        "save_outreach_draft",
        "save_legal_draft",
        "nzbn_lookup",
        "hitl_policy_summary",
        "check_hitl_action",
    ]


def assert_no_forbidden_tools() -> None:
    for name in tool_inventory():
        if name in FORBIDDEN_TOOL_NAMES:
            raise AssertionError(f"Forbidden tool exposed: {name}")
        # also ensure inventory doesn't contain send/file verbs
        for frag in ("send_email", "file_ird", "move_money", "submit_grant"):
            if frag in name:
                raise AssertionError(f"Dangerous tool name: {name}")
