"""HITL hard stops — tools that must never exist or always block."""
from __future__ import annotations

from dataclasses import dataclass

# Tools we deliberately do not expose on the MCP surface
FORBIDDEN_TOOL_NAMES = frozenset(
    {
        "send_email",
        "send_sms",
        "send_message",
        "file_companies_office",
        "file_ird",
        "file_gst",
        "move_money",
        "make_payment",
        "create_payment",
        "create_xero_invoice",
        "submit_grant",
        "sign_document",
        "realme_login",
        "email_digest",
        "file_gst_return",
        "bank_transfer",
        "email_handoff",
        "claim_gst",
        "send_pilot_offer",
        "email_partner_report",
        # hardened expansions
        "webhook_exfil",
        "upload_customer_data",
        "disable_hitl",
        "bypass_guardrails",
        "auto_approve",
        "mass_mail",
        "scraped_lead_blast",
    }
)

WATERMARKS = {
    "draft": "DRAFT — NOT FOR SUBMISSION",
    "legal": "DRAFT — NOT LEGAL ADVICE — independent NZ legal review required",
    "finance": "NOT FINANCIAL ADVICE — FMCA regime may apply",
    "compliance": "INFORMATION ONLY — not a compliance certificate",
    "outreach": "DRAFT_NOT_SENT — human must send (UEM Act 2007)",
    "agent": "PREPARED BY AGENT — human must verify before use",
}


@dataclass
class HitlDecision:
    allowed: bool
    reason: str
    requires_human: bool = True


def check_action(action: str) -> HitlDecision:
    """Block known high-risk verbs even if a future tool is misnamed."""
    a = action.lower().strip()
    blocked_fragments = (
        "send_email",
        "send mail",
        "file with",
        "file_companies",
        "file_ird",
        "submit application",
        "move money",
        "wire transfer",
        "pay invoice",
        "create payment",
        "create invoice in xero",
        "sign as",
        "realme",
        "email digest",
        "auto-email",
        "file gst",
        "file myir",
        "bank transfer",
        "email handoff",
        "claim gst automatically",
        "bypass hitl",
        "disable guardrail",
        "mass mail",
        "cold email blast",
        "upload all customer",
        "exfiltrate",
    )
    for frag in blocked_fragments:
        if frag in a:
            return HitlDecision(
                allowed=False,
                reason=f"Blocked by HITL policy: '{frag}' requires a human. "
                "Agents may only inform, draft, prepare, monitor, and remind.",
                requires_human=True,
            )
    return HitlDecision(allowed=True, reason="ok", requires_human=False)


def assert_tool_name_allowed(name: str) -> None:
    if name in FORBIDDEN_TOOL_NAMES:
        raise PermissionError(
            f"Tool '{name}' is forbidden under NZ Start-Up HITL policy "
            "(agents must not file, send, pay, or sign)."
        )
