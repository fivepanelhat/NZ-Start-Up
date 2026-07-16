"""Draft artefact writers — never send."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from nz_startup.audit import append_audit
from nz_startup.hitl import WATERMARKS, check_action
from nz_startup.memory import ensure_exists


def save_outreach_draft(
    company_id: str,
    *,
    subject: str,
    body: str,
    to_hint: str = "",
    icp_segment: str = "",
) -> Path:
    decision = check_action("save_outreach_draft")
    if not decision.allowed:
        raise PermissionError(decision.reason)

    company = ensure_exists(company_id)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_subj = "".join(c if c.isalnum() or c in "-_" else "-" for c in subject)[:40]
    path = company / "drafts" / "outreach" / f"{ts}-{safe_subj or 'draft'}.md"
    content = f"""# {WATERMARKS['outreach']}

- Status: DRAFT_NOT_SENT
- To hint: {to_hint}
- ICP segment: {icp_segment}
- Created: {ts}

## Subject

{subject}

## Body

{body}

## Human send checklist

- [ ] Accurate identity
- [ ] Lawful basis / consent where required (UEM Act 2007)
- [ ] Unsubscribe / contact path if marketing
- [ ] No misleading claims
- [ ] Human clicks send in their own mail client
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    append_audit(
        company,
        actor="agent:gtm-pipeline-rep",
        skill="gtm-pipeline-rep",
        action="save_outreach_draft",
        summary=f"Draft outreach: {subject[:80]}",
        artefact_ref=str(path.relative_to(company)),
        hitl_required=True,
        hitl_status="pending",
        risk_level="medium",
        tier="gold",
    )
    return path


def save_legal_draft(company_id: str, *, title: str, body: str, doc_type: str = "general") -> Path:
    company = ensure_exists(company_id)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in title)[:40]
    path = company / "drafts" / "legal" / f"{ts}-{safe or 'draft'}.md"
    content = f"""# {WATERMARKS['legal']}

- Doc type: {doc_type}
- Status: DRAFT
- Created: {ts}

## {title}

{body}

## Open issues for NZ lawyer

- [ ]
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    append_audit(
        company,
        actor="agent:legal-document-assistant",
        skill="legal-document-assistant",
        action="save_legal_draft",
        summary=f"Legal draft: {title[:80]}",
        artefact_ref=str(path.relative_to(company)),
        hitl_required=True,
        hitl_status="pending",
        risk_level="high",
        tier="gold",
    )
    return path
