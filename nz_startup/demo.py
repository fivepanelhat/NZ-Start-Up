"""
EDA / accelerator demo walkthrough — produces a shareable DEMO report.

Safe by default: uses sample data, never sends email or files government forms.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

from nz_startup import (
    __version__,
    bank_feed,
    calendar_ops,
    grants,
    gst_worksheet,
    handoff,
    invoice_triage,
    memory,
    pipeline,
    weekly,
    xero_readonly,
)
from nz_startup.paths import company_dir, repo_root


def _step(name: str, fn: Callable[[], Any]) -> dict[str, Any]:
    try:
        result = fn()
        return {"step": name, "ok": True, "result": result}
    except Exception as e:  # noqa: BLE001 — demo continues
        return {"step": name, "ok": False, "error": str(e)}


def run_demo(
    company_id: str,
    *,
    partner: str = "Venture Taranaki",
    programme: str = "PowerUp / founder demo",
    quick: bool = False,
) -> dict[str, Any]:
    """
    Run an end-to-end demo against company memory.
    Creates company if missing. Uses sample templates from the repo.
    """
    started = datetime.now(timezone.utc)
    log: list[dict[str, Any]] = []

    def ensure_co():
        try:
            return str(memory.init_company(company_id))
        except FileExistsError:
            return str(company_dir(company_id))

    log.append(_step("init_company", ensure_co))

    sample_bank = repo_root() / "templates" / "bank-feed-sample.csv"
    sample_inv = repo_root() / "templates" / "sample-tax-invoice.txt"

    log.append(
        _step(
            "pipeline_seed",
            lambda: pipeline.add_deal(
                company_id,
                account=partner,
                stage="discovery",
                next_step="show weekly board + handoff pack",
                source="demo",
                notes=f"EDA demo for {programme}",
            )
            if not any(
                (d.get("account") or "") == partner for d in pipeline.list_deals(company_id)
            )
            else {"skipped": "partner already in pipeline"},
        )
    )

    soon = date.today().isoformat()
    log.append(
        _step(
            "calendar_demo_item",
            lambda: calendar_ops.add_item(
                company_id,
                item=f"Demo follow-up — {partner}",
                due=soon,
                category="gtm",
                notes="Demo script created this reminder",
            ),
        )
    )

    if not quick:
        log.append(
            _step(
                "grants_seed",
                lambda: grants.seed_nz_starters(company_id) or "already seeded or added",
            )
        )
        log.append(
            _step(
                "xero_offline",
                lambda: str(
                    xero_readonly.write_snapshot(
                        company_id,
                        xero_readonly.fetch_snapshot(company_id, force_offline=True),
                    )["markdown"]
                ),
            )
        )
        log.append(
            _step(
                "bank_import",
                lambda: bank_feed.import_csv(company_id, sample_bank, replace=False),
            )
        )
        log.append(
            _step(
                "gst_prepare",
                lambda: {
                    "net_gst_est": gst_worksheet.prepare_and_write(
                        company_id,
                        period_start=f"{date.today().year}-07-01",
                        period_end=f"{date.today().year}-07-31",
                    )[0]["gst_estimate"]["net_gst_est"]
                },
            )
        )
        log.append(
            _step(
                "invoice_triage",
                lambda: invoice_triage.triage_file(company_id, sample_inv)["parsed"][
                    "invoice_number"
                ],
            )
        )
        log.append(
            _step(
                "handoff_pack",
                lambda: str(handoff.create_handoff_pack(company_id, label="demo")["latest"]),
            )
        )

    log.append(
        _step(
            "weekly_board",
            lambda: str(weekly.generate_weekly_review(company_id)),
        )
    )

    report = {
        "title": f"NZ Start-Up in a Box — demo for {partner}",
        "programme": programme,
        "company_id": company_id,
        "partner": partner,
        "product_version": __version__,
        "started_at": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "finished_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "quick": quick,
        "steps": log,
        "talking_points": [
            "Jurisdiction depth is the moat — Companies Office, IRD, RDTI, regional grants — not agent hype",
            "Autonomy ceiling is the product: draft/prepare only; humans file, send, pay",
            "Weekly board report is the founder experience and the EDA demo artefact",
            "White-label path: cohort seats for EDAs without multi-tenant SaaS risk yet",
            "Finance loop ends in accountant handoff zip — not automated tax agent behaviour",
        ],
        "hitl": (
            "Agents inform, draft, prepare, monitor, and remind. "
            "Humans advise, sign, file, send, and pay."
        ),
        "next_human_actions": [
            f"Book discovery with {partner} contacts from pipeline",
            "Review weekly board markdown and handoff zip",
            "Decide paid pilot offer pricing before free pilots",
            "If cohort interest: nz-startup cohort init + add-seat + pack",
        ],
    }

    # Write report into company memory
    out_dir = company_dir(company_id) / "demo"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    json_path = out_dir / f"demo-report-{stamp}.json"
    md_path = out_dir / f"demo-report-{stamp}.md"
    latest_md = out_dir / "demo-report-latest.md"
    latest_json = out_dir / "demo-report-latest.json"
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    md = format_demo_markdown(report)
    md_path.write_text(md, encoding="utf-8", newline="\n")
    latest_md.write_text(md, encoding="utf-8", newline="\n")
    latest_json.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    report["paths"] = {
        "markdown": str(md_path),
        "json": str(json_path),
        "latest_md": str(latest_md),
    }
    return report


def format_demo_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report.get('title')}",
        "",
        f"- Partner: **{report.get('partner')}**",
        f"- Programme: {report.get('programme')}",
        f"- Company memory: `{report.get('company_id')}`",
        f"- Product version: {report.get('product_version')}",
        f"- Started: {report.get('started_at')}",
        f"- Finished: {report.get('finished_at')}",
        f"- Mode: {'quick' if report.get('quick') else 'full'}",
        "",
        "## Autonomy slogan",
        "",
        report.get("hitl", ""),
        "",
        "## Steps run",
        "",
    ]
    for s in report.get("steps") or []:
        status = "OK" if s.get("ok") else "FAIL"
        detail = s.get("error") if not s.get("ok") else _short(s.get("result"))
        lines.append(f"- **{s.get('step')}** — {status}: {detail}")
    lines.extend(["", "## Talking points (for the room)", ""])
    for i, t in enumerate(report.get("talking_points") or [], 1):
        lines.append(f"{i}. {t}")
    lines.extend(["", "## Next human actions", ""])
    for a in report.get("next_human_actions") or []:
        lines.append(f"- [ ] {a}")
    lines.extend(
        [
            "",
            "## Close",
            "",
            "This demo did **not** send email, file with IRD/Companies Office, or move money.",
            "White-label packaging available via `nz-startup cohort pack`.",
            "",
        ]
    )
    return "\n".join(lines)


def _short(value: Any, limit: int = 120) -> str:
    if value is None:
        return "—"
    if isinstance(value, (dict, list)):
        text = json.dumps(value, default=str)
    else:
        text = str(value)
    text = text.replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 3] + "..."
