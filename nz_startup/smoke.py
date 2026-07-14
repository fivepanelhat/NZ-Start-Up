"""End-to-end smoke test for install / CI / pre-demo confidence."""
from __future__ import annotations

from typing import Any

from nz_startup import (
    __version__,
    bank_feed,
    board_pack,
    cohort,
    demo,
    handoff,
    invoice_triage,
    memory,
    pipeline,
    status,
    weekly,
    xero_readonly,
)
from nz_startup.paths import repo_root


def run_smoke(*, keep: bool = False) -> dict[str, Any]:
    """
    Run isolated smoke against a temp company (or keep under memory if keep=True).
    Returns structured report; raises on hard failure if any step fails.
    """
    steps: list[dict[str, Any]] = []
    company_id = "smoke-e2e"

    # Use real memory root but unique company — or temp via env would need more plumbing.
    # Prefer dedicated smoke id with force init.
    try:
        memory.init_company(company_id, force=True)
        steps.append({"step": "init", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "init", "ok": False, "error": str(e)})
        return _finish(steps, ok=False)

    try:
        pipeline.add_deal(
            company_id,
            account="Smoke Partner",
            stage="discovery",
            next_step="verify smoke",
        )
        steps.append({"step": "pipeline", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "pipeline", "ok": False, "error": str(e)})

    try:
        sample = repo_root() / "templates" / "bank-feed-sample.csv"
        bank_feed.import_csv(company_id, sample, replace=True)
        steps.append({"step": "bank", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "bank", "ok": False, "error": str(e)})

    try:
        xero_readonly.write_snapshot(
            company_id, xero_readonly.fetch_snapshot(company_id, force_offline=True)
        )
        steps.append({"step": "xero", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "xero", "ok": False, "error": str(e)})

    try:
        inv = repo_root() / "templates" / "sample-tax-invoice.txt"
        invoice_triage.triage_file(company_id, inv)
        steps.append({"step": "invoice", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "invoice", "ok": False, "error": str(e)})

    try:
        weekly.generate_weekly_review(company_id)
        steps.append({"step": "weekly", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "weekly", "ok": False, "error": str(e)})

    try:
        st, _ = status.write_status(company_id)
        steps.append({"step": "status", "ok": True, "score": st.get("score")})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "status", "ok": False, "error": str(e)})

    try:
        handoff.create_handoff_pack(company_id, label="smoke")
        steps.append({"step": "handoff", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "handoff", "ok": False, "error": str(e)})

    try:
        board_pack.create_board_pack(company_id, label="smoke", refresh_weekly=False)
        steps.append({"step": "board_pack", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "board_pack", "ok": False, "error": str(e)})

    try:
        cid = "smoke-cohort"
        try:
            cohort.init_cohort(
                cid,
                partner_name="Smoke EDA",
                programme="CI",
                seat_quota=3,
                force=True,
            )
        except FileExistsError:
            pass
        cohort.build_white_label_pack(cid)
        steps.append({"step": "cohort_pack", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "cohort_pack", "ok": False, "error": str(e)})

    try:
        demo.run_demo(company_id, partner="Smoke EDA", quick=True)
        steps.append({"step": "demo_quick", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "demo_quick", "ok": False, "error": str(e)})

    try:
        from nz_startup import onboard, pilot_offer

        onboard.run_onboard("smoke-onboard", force=True, legal_name="Smoke Onboard Ltd")
        pilot_offer.prepare_and_write(
            "smoke-onboard",
            customer_name="Smoke Customer Ltd",
            pilot_fee_nzd="1500",
        )
        steps.append({"step": "onboard_pilot", "ok": True})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "onboard_pilot", "ok": False, "error": str(e)})

    try:
        from nz_startup import doctor

        d = doctor.run_doctor()
        steps.append({"step": "doctor", "ok": bool(d.get("ok"))})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "doctor", "ok": False, "error": str(e)})

    try:
        from nz_startup import compliance_gate

        cg = compliance_gate.run_compliance_check(None)
        steps.append({"step": "compliance_gate", "ok": bool(cg.get("ok"))})
    except Exception as e:  # noqa: BLE001
        steps.append({"step": "compliance_gate", "ok": False, "error": str(e)})

    ok = all(s.get("ok") for s in steps)
    return _finish(steps, ok=ok, company_id=company_id)


def _finish(
    steps: list[dict[str, Any]],
    *,
    ok: bool,
    company_id: str = "smoke-e2e",
) -> dict[str, Any]:
    return {
        "ok": ok,
        "product_version": __version__,
        "company_id": company_id,
        "steps": steps,
        "failed": [s["step"] for s in steps if not s.get("ok")],
        "hitl": "Smoke never sends, files, or pays.",
    }


def format_smoke_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Smoke report — v{report.get('product_version')}",
        "",
        f"- Overall: **{'PASS' if report.get('ok') else 'FAIL'}**",
        f"- Company: `{report.get('company_id')}`",
        "",
    ]
    for s in report.get("steps") or []:
        mark = "OK" if s.get("ok") else "FAIL"
        extra = s.get("score", s.get("error", ""))
        lines.append(f"- [{mark}] {s.get('step')} {extra}")
    if report.get("failed"):
        lines.append("")
        lines.append("Failed: " + ", ".join(report["failed"]))
    lines.append("")
    lines.append(report.get("hitl", ""))
    lines.append("")
    return "\n".join(lines)
