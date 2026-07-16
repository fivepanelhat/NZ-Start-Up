"""
Xero read-only adapter.

HITL / product rules:
- Read organisation, invoices, bank summary only.
- Never create invoices, payments, contacts, or bank transfers.
- Without credentials: offline demo snapshot (clearly labelled).
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

XERO_API = "https://api.xero.com/api.xro/2.0"
XERO_TOKEN_URL = "https://identity.xero.com/connect/token"

# Tools / verbs we must never implement
FORBIDDEN_XERO_WRITES = frozenset(
    {
        "create_invoice",
        "create_payment",
        "create_bank_transaction",
        "void_invoice",
        "update_contact",
    }
)


class XeroError(RuntimeError):
    pass


def _access_token() -> str | None:
    return os.environ.get("XERO_ACCESS_TOKEN") or None


def _tenant_id() -> str | None:
    return os.environ.get("XERO_TENANT_ID") or None


def _client_id() -> str | None:
    return os.environ.get("XERO_CLIENT_ID") or None


def _client_secret() -> str | None:
    return os.environ.get("XERO_CLIENT_SECRET") or None


def _refresh_token() -> str | None:
    return os.environ.get("XERO_REFRESH_TOKEN") or None


def credentials_status() -> dict[str, Any]:
    return {
        "has_access_token": bool(_access_token()),
        "has_tenant_id": bool(_tenant_id()),
        "has_client_id": bool(_client_id()),
        "has_refresh_token": bool(_refresh_token()),
        "mode": "live" if (_access_token() and _tenant_id()) else "offline",
        "note": "Read-only. Never store tokens in company memory or git.",
    }


def refresh_access_token() -> dict[str, str]:
    """
    Exchange refresh token for a new access token (optional).
    Returns tokens; does not write them to disk — caller must set env.
    """
    cid, secret, refresh = _client_id(), _client_secret(), _refresh_token()
    if not (cid and secret and refresh):
        raise XeroError(
            "Need XERO_CLIENT_ID, XERO_CLIENT_SECRET, and XERO_REFRESH_TOKEN to refresh"
        )
    data = urllib.parse.urlencode(
        {
            "grant_type": "refresh_token",
            "refresh_token": refresh,
            "client_id": cid,
            "client_secret": secret,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        XERO_TOKEN_URL,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "nz-startup-in-a-box/0.4 (xero-readonly)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:400]
        raise XeroError(f"Xero token refresh HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise XeroError(f"Xero token network error: {e}") from e
    return {
        "access_token": payload.get("access_token", ""),
        "refresh_token": payload.get("refresh_token", refresh),
        "expires_in": str(payload.get("expires_in", "")),
        "token_type": payload.get("token_type", "Bearer"),
        "warning": "Set XERO_ACCESS_TOKEN in your environment; do not commit tokens.",
    }


def _xero_get(path: str) -> dict[str, Any]:
    token, tenant = _access_token(), _tenant_id()
    if not token or not tenant:
        raise XeroError("XERO_ACCESS_TOKEN and XERO_TENANT_ID required for live calls")
    url = f"{XERO_API.rstrip('/')}/{path.lstrip('/')}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Xero-tenant-id": tenant,
            "Accept": "application/json",
            "User-Agent": "nz-startup-in-a-box/0.4 (xero-readonly)",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise XeroError(f"Xero API HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise XeroError(f"Xero API network error: {e}") from e


def offline_snapshot(company_id: str) -> dict[str, Any]:
    return {
        "mode": "offline",
        "company_id": company_id,
        "as_of": date.today().isoformat(),
        "organisation": {
            "Name": "DEMO — set XERO_ACCESS_TOKEN + XERO_TENANT_ID for live read",
        },
        "invoices_summary": {
            "count": 0,
            "authorised_total_approx": None,
            "note": "No live data",
        },
        "accounts_summary": {"count": 0},
        "hitl": "Read-only adapter. Human/accountant files GST and moves money.",
        "setup": [
            "Create a Xero app with accounting.transactions.read (or readonly) scopes",
            "Complete OAuth and set XERO_ACCESS_TOKEN + XERO_TENANT_ID",
            "Optional refresh: XERO_CLIENT_ID, XERO_CLIENT_SECRET, XERO_REFRESH_TOKEN",
            "Never commit tokens; never enable write scopes for this product path",
        ],
    }


def live_snapshot() -> dict[str, Any]:
    org = _xero_get("Organisation")
    invoices = _xero_get("Invoices?Statuses=AUTHORISED&page=1")
    accounts = _xero_get("Accounts")

    inv_list = invoices.get("Invoices") or []
    total = 0.0
    for inv in inv_list:
        try:
            total += float(inv.get("Total") or 0)
        except (TypeError, ValueError):
            pass

    org_list = org.get("Organisations") or []
    org0 = org_list[0] if org_list else {}
    acc_list = accounts.get("Accounts") or []

    return {
        "mode": "live",
        "as_of": date.today().isoformat(),
        "organisation": {
            "Name": org0.get("Name"),
            "LegalName": org0.get("LegalName"),
            "BaseCurrency": org0.get("BaseCurrency"),
            "CountryCode": org0.get("CountryCode"),
            "OrganisationStatus": org0.get("OrganisationStatus"),
        },
        "invoices_summary": {
            "count": len(inv_list),
            "authorised_total_approx": round(total, 2),
            "sample": [
                {
                    "InvoiceNumber": i.get("InvoiceNumber"),
                    "Contact": (i.get("Contact") or {}).get("Name"),
                    "Total": i.get("Total"),
                    "DueDateString": i.get("DueDateString") or i.get("DueDate"),
                    "Status": i.get("Status"),
                }
                for i in inv_list[:10]
            ],
        },
        "accounts_summary": {
            "count": len(acc_list),
            "sample_names": [a.get("Name") for a in acc_list[:15] if a.get("Name")],
        },
        "hitl": "Read-only. Do not treat totals as audited financials.",
    }


def fetch_snapshot(company_id: str, *, force_offline: bool = False) -> dict[str, Any]:
    if force_offline or credentials_status()["mode"] != "live":
        snap = offline_snapshot(company_id)
    else:
        try:
            snap = live_snapshot()
            snap["company_id"] = company_id
        except XeroError as e:
            snap = offline_snapshot(company_id)
            snap["live_error"] = str(e)
            snap["mode"] = "offline_fallback"
    snap["fetched_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return snap


def write_snapshot(company_id: str, snapshot: dict[str, Any] | None = None) -> dict[str, Path]:
    """Persist snapshot under company memory (no tokens)."""
    company = ensure_exists(company_id)
    snap = snapshot or fetch_snapshot(company_id)
    # Redact any accidental token-like keys
    for key in list(snap.keys()):
        if "token" in key.lower() or "secret" in key.lower():
            snap.pop(key, None)

    finance_dir = company / "finance"
    finance_dir.mkdir(parents=True, exist_ok=True)
    json_path = finance_dir / "xero-snapshot.json"
    json_path.write_text(json.dumps(snap, indent=2, default=str) + "\n", encoding="utf-8")

    md_path = finance_dir / "xero-snapshot.md"
    md_path.write_text(format_snapshot_markdown(snap), encoding="utf-8", newline="\n")

    # Update runway.md with non-secret high-level note only
    runway = company / "runway.md"
    note = (
        f"\n\n## Xero snapshot ({snap.get('as_of')})\n"
        f"- Mode: `{snap.get('mode')}`\n"
        f"- Org: {(snap.get('organisation') or {}).get('Name', '—')}\n"
        f"- Authorised invoices (sample page): "
        f"{(snap.get('invoices_summary') or {}).get('count', 0)}\n"
        f"- Detail: `finance/xero-snapshot.md`\n"
        f"- HITL: human/accountant files tax and moves money\n"
    )
    if runway.exists():
        existing = runway.read_text(encoding="utf-8")
        if "## Xero snapshot" in existing:
            # replace trailing section roughly
            head = existing.split("## Xero snapshot")[0].rstrip()
            runway.write_text(head + note, encoding="utf-8", newline="\n")
        else:
            runway.write_text(existing.rstrip() + note, encoding="utf-8", newline="\n")
    else:
        runway.write_text("# Runway Snapshot\n" + note, encoding="utf-8", newline="\n")

    append_audit(
        company,
        actor="agent:finance-clerk",
        skill="finance-clerk",
        action="xero_readonly_snapshot",
        summary=f"Xero snapshot mode={snap.get('mode')}",
        artefact_ref="finance/xero-snapshot.json",
        tier="diamond",
        risk_level="medium",
        hitl_required=False,
    )
    return {"json": json_path, "markdown": md_path, "runway": runway}


def format_snapshot_markdown(snap: dict[str, Any]) -> str:
    org = snap.get("organisation") or {}
    inv = snap.get("invoices_summary") or {}
    lines = [
        "# Xero read-only snapshot",
        "",
        f"- Mode: `{snap.get('mode')}`",
        f"- As of: {snap.get('as_of')}",
        f"- Fetched: {snap.get('fetched_at', '—')}",
        f"- HITL: {snap.get('hitl', 'Read-only')}",
        "",
        "## Organisation",
        "",
        f"- Name: {org.get('Name', '—')}",
        f"- Legal: {org.get('LegalName', '—')}",
        f"- Currency: {org.get('BaseCurrency', '—')}",
        f"- Country: {org.get('CountryCode', '—')}",
        "",
        "## Authorised invoices (first page)",
        "",
        f"- Count: {inv.get('count', 0)}",
        f"- Total approx: {inv.get('authorised_total_approx', '—')}",
        "",
    ]
    for sample in inv.get("sample") or []:
        lines.append(
            f"- {sample.get('InvoiceNumber')} · {sample.get('Contact')} · "
            f"{sample.get('Total')} · due {sample.get('DueDateString')} · {sample.get('Status')}"
        )
    if snap.get("mode") in ("offline", "offline_fallback"):
        lines.extend(["", "## Setup", ""])
        for s in snap.get("setup") or []:
            lines.append(f"- {s}")
        if snap.get("live_error"):
            lines.append(f"- Live error: {snap['live_error']}")
    lines.extend(
        [
            "",
            "## Forbidden",
            "",
            "- This adapter does not create payments, invoices, or bank transactions.",
            "- NOT a tax filing. Human or accountant uses myIR / Xero UI for filings.",
            "",
        ]
    )
    return "\n".join(lines)
