"""
HITL-safe MCP server for NZ Start-Up in a Box.

Exposes draft/prepare/read tools only. Deliberately omits send/file/pay/sign.
"""
from __future__ import annotations

import json

from nz_startup import (
    __version__,
    bank_feed,
    calendar_ops,
    drafts,
    export_reminders,
    grants,
    gst_worksheet,
    handoff,
    invoice_triage,
    memory,
    nzbn,
    pipeline,
    rdti,
    weekly,
    xero_readonly,
)
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
            "NZ Start-Up in a Box fleet connectors v0.4. "
            "Agents may inform, draft, prepare, monitor, and remind. "
            "Humans must advise, sign, file, send, and pay. "
            f"Forbidden tools: {sorted(FORBIDDEN_TOOL_NAMES)}. "
            "Pipeline is CRM-lite local only — never send outreach. "
            "Grants tracker never submits applications. "
            "Xero adapter is read-only — never create payments. "
            "Reminder exports write files only — never email digests. "
            "Bank import is CSV-only triage — never moves money. "
            "GST prepare builds working papers only — never files myIR. "
            "Invoice triage extracts fields for review — never claims GST. "
            "Handoff pack writes a local zip — never emails the accountant. "
            "Always load CAT Gold/Diamond/Platinum classification for material work."
        ),
    )

    @mcp.tool()
    def list_companies() -> list[str]:
        """List local company memory IDs under memory/companies/."""
        return memory.list_companies()

    @mcp.tool()
    def init_company_memory(company_id: str, force: bool = False) -> str:
        """Create company memory from the example scaffold (local only). Seeds pipeline/calendar/grants."""
        path = memory.init_company(company_id, force=force)
        return f"Initialised {path} with pipeline, calendar, grants trackers"

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
        """Append a contemporaneous RDTI R&D activity row. Never invent hours."""
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
        """Generate a weekly board review with pipeline, calendar reminders, and grants."""
        path = weekly.generate_weekly_review(company_id, review_date or None)
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
        """Save an outreach email draft. NEVER sends (UEM Act 2007)."""
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
        """Read-only NZBN / entity name lookup. Never files with Companies Office."""
        result = nzbn.lookup_entities(query, limit=limit)
        return nzbn.format_lookup_markdown(result)

    # --- Pipeline (v0.3) ---

    @mcp.tool()
    def pipeline_list(company_id: str, stage: str = "") -> str:
        """List pipeline deals; optional stage filter (lead/discovery/.../won/lost)."""
        rows = pipeline.list_deals(company_id, stage=stage or None)
        return json.dumps(rows, indent=2)

    @mcp.tool()
    def pipeline_add(
        company_id: str,
        account: str,
        stage: str = "lead",
        next_step: str = "",
        owner: str = "Founder",
        value_nzd: str = "",
        source: str = "",
        notes: str = "",
    ) -> str:
        """Add a local CRM deal. Does not contact the account."""
        row = pipeline.add_deal(
            company_id,
            account=account,
            stage=stage,
            next_step=next_step,
            owner=owner,
            value_nzd=value_nzd,
            source=source,
            notes=notes,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def pipeline_update(
        company_id: str,
        deal_id: str,
        stage: str = "",
        next_step: str = "",
        owner: str = "",
        value_nzd: str = "",
        notes: str = "",
    ) -> str:
        """Update deal stage or next step. Never sends outreach."""
        row = pipeline.update_deal(
            company_id,
            deal_id,
            stage=stage or None,
            next_step=next_step if next_step != "" else None,
            owner=owner or None,
            value_nzd=value_nzd if value_nzd != "" else None,
            notes=notes if notes != "" else None,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def pipeline_summary(company_id: str) -> str:
        """Markdown pipeline summary for board review."""
        return pipeline.format_summary_markdown(company_id)

    # --- Calendar (v0.3) ---

    @mcp.tool()
    def calendar_list(company_id: str, status: str = "") -> str:
        """List calendar items; optional status filter."""
        return json.dumps(calendar_ops.list_items(company_id, status=status or None), indent=2)

    @mcp.tool()
    def calendar_add(
        company_id: str,
        item: str,
        due: str,
        owner: str = "Founder",
        status: str = "planned",
        category: str = "compliance",
        recurring: str = "",
        notes: str = "",
    ) -> str:
        """Add a calendar deadline. Agent reminds; human files."""
        row = calendar_ops.add_item(
            company_id,
            item=item,
            due=due,
            owner=owner,
            status=status,
            category=category,
            recurring=recurring,
            notes=notes,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def calendar_update(
        company_id: str,
        item_id: str,
        due: str = "",
        status: str = "",
        owner: str = "",
        notes: str = "",
        item: str = "",
    ) -> str:
        """Update a calendar item."""
        row = calendar_ops.update_item(
            company_id,
            item_id,
            due=due or None,
            status=status or None,
            owner=owner or None,
            notes=notes if notes != "" else None,
            item=item or None,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def calendar_reminders(company_id: str, within_days: int = 14) -> str:
        """Upcoming and overdue deadline reminders (not a compliance certificate)."""
        return calendar_ops.format_reminders_markdown(company_id, within_days=within_days)

    # --- Grants (v0.3) ---

    @mcp.tool()
    def grants_list(company_id: str, status: str = "") -> str:
        """List tracked grant opportunities."""
        return json.dumps(grants.list_grants(company_id, status=status or None), indent=2)

    @mcp.tool()
    def grants_add(
        company_id: str,
        name: str,
        funder: str = "",
        status: str = "watch",
        fit_score: str = "",
        deadline: str = "",
        amount_hint: str = "",
        url: str = "",
        next_action: str = "",
        notes: str = "",
    ) -> str:
        """Add a grant to the tracker. Does not submit applications."""
        row = grants.add_grant(
            company_id,
            name=name,
            funder=funder,
            status=status,
            fit_score=fit_score,
            deadline=deadline,
            amount_hint=amount_hint,
            url=url,
            next_action=next_action,
            notes=notes,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def grants_update(
        company_id: str,
        grant_id: str,
        status: str = "",
        fit_score: str = "",
        deadline: str = "",
        next_action: str = "",
        notes: str = "",
        url: str = "",
    ) -> str:
        """Update grant tracker row. Status 'submitted' requires human confirmation note."""
        row = grants.update_grant(
            company_id,
            grant_id,
            status=status or None,
            fit_score=fit_score if fit_score != "" else None,
            deadline=deadline if deadline != "" else None,
            next_action=next_action if next_action != "" else None,
            notes=notes if notes != "" else None,
            url=url if url != "" else None,
        )
        return json.dumps(row, indent=2)

    @mcp.tool()
    def grants_rank(company_id: str, min_score: int = 0) -> str:
        """Rank open opportunities by fit score."""
        return json.dumps(grants.rank_by_fit(company_id, min_score=min_score), indent=2)

    @mcp.tool()
    def xero_status() -> str:
        """Report whether Xero live credentials are configured (never prints secrets)."""
        return json.dumps(xero_readonly.credentials_status(), indent=2)

    @mcp.tool()
    def xero_snapshot(company_id: str, force_offline: bool = False) -> str:
        """
        Read-only Xero snapshot into company memory (finance/xero-snapshot.*).
        Without tokens returns offline demo guidance. Never creates payments.
        """
        snap = xero_readonly.fetch_snapshot(company_id, force_offline=force_offline)
        paths = xero_readonly.write_snapshot(company_id, snap)
        return (
            xero_readonly.format_snapshot_markdown(snap)
            + "\n\n## Written\n"
            + "\n".join(f"- {k}: {v}" for k, v in paths.items())
        )

    @mcp.tool()
    def export_deadline_reminders(
        company_id: str,
        digest_days: int = 14,
        ics_days: int = 90,
    ) -> str:
        """
        Export ICS + markdown deadline digest under company exports/.
        Does not email. Human may import ICS into their calendar app.
        """
        paths = export_reminders.export_all(
            company_id, within_days=digest_days, ics_days=ics_days
        )
        return json.dumps({k: str(v) for k, v in paths.items()}, indent=2)

    @mcp.tool()
    def bank_import_csv(
        company_id: str,
        file_path: str,
        replace: bool = False,
        batch_label: str = "",
    ) -> str:
        """
        Import a bank CSV export for triage. Never moves money or calls bank APIs.
        file_path must be a local path the human exported.
        """
        from pathlib import Path

        summary = bank_feed.import_csv(
            company_id,
            Path(file_path),
            replace=replace,
            batch_label=batch_label or None,
        )
        return json.dumps(summary, indent=2, default=str)

    @mcp.tool()
    def bank_triage(company_id: str) -> str:
        """Summarise imported bank feed categories and GST hints."""
        return bank_feed.format_triage_markdown(company_id)

    @mcp.tool()
    def gst_prepare_worksheet(
        company_id: str,
        period_start: str,
        period_end: str,
        gst_rate: float = 0.15,
        label: str = "",
    ) -> str:
        """
        Build GST working papers from bank feed + Xero snapshot for a period.
        NOT a tax filing — human/accountant files in myIR.
        """
        ws, paths = gst_worksheet.prepare_and_write(
            company_id,
            period_start=period_start,
            period_end=period_end,
            gst_rate=gst_rate,
            label=label or None,
        )
        return (
            gst_worksheet.format_worksheet_markdown(ws)
            + "\n\n## Written\n"
            + "\n".join(f"- {k}: {v}" for k, v in paths.items())
        )

    @mcp.tool()
    def invoice_triage_path(company_id: str, path: str) -> str:
        """
        Triage an invoice file or folder (PDF/text). Extracts fields for human review.
        Requires pypdf for best PDF text extraction (optional extra). Never claims GST.
        """
        from pathlib import Path

        results = invoice_triage.triage_path(company_id, Path(path))
        return json.dumps(results, indent=2, default=str)

    @mcp.tool()
    def invoice_list(company_id: str) -> str:
        """List triaged invoices from the local registry."""
        return invoice_triage.format_registry_summary(company_id)

    @mcp.tool()
    def handoff_pack_create(company_id: str, label: str = "accountant") -> str:
        """
        Create a local zip of finance working papers for an accountant.
        Does not email or upload — human delivers the zip.
        """
        result = handoff.create_handoff_pack(company_id, label=label)
        return json.dumps(
            {k: (str(v) if hasattr(v, "__fspath__") else v) for k, v in result.items()},
            indent=2,
        )

    @mcp.tool()
    def hitl_policy_summary() -> str:
        """Return autonomy ceilings and forbidden actions for this fleet."""
        return (
            "Agents: inform, draft, prepare, monitor, remind.\n"
            "Humans: advise, sign, file, send, pay.\n"
            f"Forbidden MCP tools (not implemented): {sorted(FORBIDDEN_TOOL_NAMES)}\n"
            f"Watermarks: {json.dumps(WATERMARKS, indent=2)}\n"
            f"Server version: {__version__}\n"
            "Xero read-only · Bank triage · GST papers · Invoice triage · Handoff zip only.\n"
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

    return mcp


def run_stdio() -> None:
    mcp = build_server()
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
        "pipeline_list",
        "pipeline_add",
        "pipeline_update",
        "pipeline_summary",
        "calendar_list",
        "calendar_add",
        "calendar_update",
        "calendar_reminders",
        "grants_list",
        "grants_add",
        "grants_update",
        "grants_rank",
        "xero_status",
        "xero_snapshot",
        "export_deadline_reminders",
        "bank_import_csv",
        "bank_triage",
        "gst_prepare_worksheet",
        "invoice_triage_path",
        "invoice_list",
        "handoff_pack_create",
        "hitl_policy_summary",
        "check_hitl_action",
    ]


def assert_no_forbidden_tools() -> None:
    for name in tool_inventory():
        if name in FORBIDDEN_TOOL_NAMES:
            raise AssertionError(f"Forbidden tool exposed: {name}")
        for frag in ("send_email", "file_ird", "move_money", "submit_grant"):
            if frag in name:
                raise AssertionError(f"Dangerous tool name: {name}")
