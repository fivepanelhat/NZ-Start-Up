"""nz-startup CLI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nz_startup import __version__
from nz_startup import (
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
from nz_startup.install_skills import default_aether_skills, install_skills
from nz_startup.paths import repo_root


def cmd_init(args: argparse.Namespace) -> int:
    path = memory.init_company(args.company_id, force=args.force)
    print(f"Initialised company memory: {path}")
    print("Seeded pipeline.csv, calendar.csv, grants-tracker.csv")
    print("Edit profile.md with non-secret facts next.")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    companies = memory.list_companies()
    if not companies:
        print("No companies yet. Run: nz-startup init <id>")
        return 0
    for c in companies:
        print(c)
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser() if args.target else default_aether_skills()
    names = install_skills(target, mode=args.mode)
    print(f"Installed {len(names)} skills → {target}")
    for n in names:
        print(f"  - {n}")
    return 0


def cmd_rdti(args: argparse.Namespace) -> int:
    if args.rdti_cmd == "add":
        row = rdti.append_entry(
            args.company_id,
            hours=args.hours,
            activity=args.activity,
            technical_uncertainty=args.uncertainty,
            evidence_ref=args.evidence,
            person=args.person,
            notes=args.notes or "",
            entry_date=args.date,
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.rdti_cmd == "list":
        rows = rdti.list_entries(args.company_id, limit=args.limit)
        print(json.dumps(rows, indent=2))
        return 0
    print("Unknown rdti subcommand", file=sys.stderr)
    return 2


def cmd_pipeline(args: argparse.Namespace) -> int:
    cid = args.company_id
    if args.pipeline_cmd == "list":
        rows = pipeline.list_deals(cid, stage=args.stage)
        print(json.dumps(rows, indent=2) if args.json else pipeline.format_summary_markdown(cid))
        return 0
    if args.pipeline_cmd == "add":
        row = pipeline.add_deal(
            cid,
            account=args.account,
            stage=args.stage or "lead",
            next_step=args.next_step or "",
            owner=args.owner or "Founder",
            value_nzd=args.value or "",
            source=args.source or "",
            notes=args.notes or "",
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.pipeline_cmd == "update":
        row = pipeline.update_deal(
            cid,
            args.deal_id,
            stage=args.stage,
            next_step=args.next_step,
            owner=args.owner,
            value_nzd=args.value,
            notes=args.notes,
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.pipeline_cmd == "summary":
        print(pipeline.format_summary_markdown(cid))
        return 0
    return 2


def cmd_calendar(args: argparse.Namespace) -> int:
    cid = args.company_id
    if args.calendar_cmd == "list":
        rows = calendar_ops.list_items(cid, status=args.status)
        print(json.dumps(rows, indent=2))
        return 0
    if args.calendar_cmd == "add":
        row = calendar_ops.add_item(
            cid,
            item=args.item,
            due=args.due,
            owner=args.owner or "Founder",
            status=args.status or "planned",
            category=args.category or "compliance",
            recurring=args.recurring or "",
            notes=args.notes or "",
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.calendar_cmd == "update":
        row = calendar_ops.update_item(
            cid,
            args.item_id,
            due=args.due,
            status=args.status,
            owner=args.owner,
            notes=args.notes,
            item=args.item,
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.calendar_cmd == "remind":
        if args.json:
            print(json.dumps(calendar_ops.reminders(cid, within_days=args.days), indent=2, default=str))
        else:
            print(calendar_ops.format_reminders_markdown(cid, within_days=args.days))
        return 0
    if args.calendar_cmd == "seed":
        rows = calendar_ops.seed_defaults(cid)
        print(json.dumps(rows, indent=2))
        return 0
    return 2


def cmd_grants(args: argparse.Namespace) -> int:
    cid = args.company_id
    if args.grants_cmd == "list":
        rows = grants.list_grants(cid, status=args.status)
        print(json.dumps(rows, indent=2))
        return 0
    if args.grants_cmd == "add":
        row = grants.add_grant(
            cid,
            name=args.name,
            funder=args.funder or "",
            status=args.status or "watch",
            fit_score=args.fit or "",
            deadline=args.deadline or "",
            amount_hint=args.amount or "",
            url=args.url or "",
            next_action=args.next_action or "",
            notes=args.notes or "",
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.grants_cmd == "update":
        row = grants.update_grant(
            cid,
            args.grant_id,
            status=args.status,
            fit_score=args.fit,
            deadline=args.deadline,
            next_action=args.next_action,
            notes=args.notes,
            url=args.url,
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.grants_cmd == "rank":
        rows = grants.rank_by_fit(cid, min_score=args.min_fit)
        print(json.dumps(rows, indent=2) if args.json else grants.format_board_slice(cid))
        return 0
    if args.grants_cmd == "seed":
        rows = grants.seed_nz_starters(cid)
        print(json.dumps(rows, indent=2))
        return 0
    return 2


def cmd_weekly(args: argparse.Namespace) -> int:
    path = weekly.generate_weekly_review(args.company_id, args.date)
    print(f"Weekly review written: {path}")
    print("HITL: founder must review and decide — agent does not decide.")
    return 0


def cmd_nzbn(args: argparse.Namespace) -> int:
    result = nzbn.lookup_entities(args.query, limit=args.limit)
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(nzbn.format_lookup_markdown(result))
    return 0


def cmd_draft_outreach(args: argparse.Namespace) -> int:
    path = drafts.save_outreach_draft(
        args.company_id,
        subject=args.subject,
        body=args.body,
        to_hint=args.to or "",
        icp_segment=args.icp or "",
    )
    print(f"Saved DRAFT_NOT_SENT: {path}")
    return 0


def cmd_xero(args: argparse.Namespace) -> int:
    if args.xero_cmd == "status":
        # company_id unused
        print(json.dumps(xero_readonly.credentials_status(), indent=2))
        return 0
    if args.xero_cmd == "snapshot":
        snap = xero_readonly.fetch_snapshot(
            args.company_id, force_offline=args.offline
        )
        paths = xero_readonly.write_snapshot(args.company_id, snap)
        if args.json:
            print(json.dumps(snap, indent=2, default=str))
        else:
            print(xero_readonly.format_snapshot_markdown(snap))
            print("---")
            for k, p in paths.items():
                print(f"{k}: {p}")
        return 0
    if args.xero_cmd == "refresh-token":
        result = xero_readonly.refresh_access_token()
        # Do not print full tokens by default — only lengths + guidance
        safe = {
            "access_token_len": len(result.get("access_token") or ""),
            "refresh_token_len": len(result.get("refresh_token") or ""),
            "expires_in": result.get("expires_in"),
            "warning": result.get("warning"),
            "hint": "Copy tokens into your private env (not git).",
        }
        if args.show_tokens:
            safe["access_token"] = result.get("access_token")
            safe["refresh_token"] = result.get("refresh_token")
        print(json.dumps(safe, indent=2))
        return 0
    return 2


def cmd_export(args: argparse.Namespace) -> int:
    if args.export_cmd == "reminders":
        paths = export_reminders.export_all(
            args.company_id,
            within_days=args.days,
            ics_days=args.ics_days,
        )
        for k, p in paths.items():
            print(f"{k}: {p}")
        return 0
    if args.export_cmd == "ics":
        text = export_reminders.build_ics(
            args.company_id, within_days=args.days
        )
        if args.stdout:
            print(text)
            return 0
        paths = export_reminders.export_all(
            args.company_id, within_days=args.days, ics_days=args.days
        )
        print(paths["ics"])
        return 0
    if args.export_cmd == "digest":
        text = export_reminders.build_digest(
            args.company_id, within_days=args.days
        )
        if args.stdout:
            print(text)
            return 0
        paths = export_reminders.export_all(
            args.company_id, within_days=args.days, ics_days=max(args.days, 90)
        )
        print(paths["digest"])
        return 0
    return 2


def cmd_bank(args: argparse.Namespace) -> int:
    if args.bank_cmd == "import":
        summary = bank_feed.import_csv(
            args.company_id,
            Path(args.file),
            replace=args.replace,
            batch_label=args.batch,
        )
        print(json.dumps(summary, indent=2, default=str))
        return 0
    if args.bank_cmd == "list":
        rows = bank_feed.list_transactions(
            args.company_id,
            direction=args.direction,
            category=args.category,
            limit=args.limit,
        )
        print(json.dumps(rows, indent=2))
        return 0
    if args.bank_cmd == "triage":
        if args.json:
            print(json.dumps(bank_feed.triage_summary(args.company_id), indent=2))
        else:
            print(bank_feed.format_triage_markdown(args.company_id))
        return 0
    return 2


def cmd_gst(args: argparse.Namespace) -> int:
    if args.gst_cmd == "prepare":
        ws, paths = gst_worksheet.prepare_and_write(
            args.company_id,
            period_start=args.start,
            period_end=args.end,
            gst_rate=args.rate,
            label=args.label,
        )
        if args.json:
            print(json.dumps(ws, indent=2, default=str))
        else:
            print(gst_worksheet.format_worksheet_markdown(ws))
            print("---")
            for k, p in paths.items():
                print(f"{k}: {p}")
        return 0
    return 2


def cmd_invoice(args: argparse.Namespace) -> int:
    if args.invoice_cmd == "triage":
        results = invoice_triage.triage_path(args.company_id, Path(args.path))
        if args.json:
            print(json.dumps(results, indent=2, default=str))
        else:
            for detail in results:
                print(invoice_triage.format_triage_markdown(detail))
                print("---")
            print(f"Triaged {len(results)} file(s). Registry: finance/invoices/invoice-registry.csv")
        return 0
    if args.invoice_cmd == "list":
        rows = invoice_triage.list_invoices(args.company_id)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            print(invoice_triage.format_registry_summary(args.company_id))
        return 0
    return 2


def cmd_handoff(args: argparse.Namespace) -> int:
    if args.handoff_cmd == "pack":
        result = handoff.create_handoff_pack(args.company_id, label=args.label)
        if args.json:
            print(
                json.dumps(
                    {k: (str(v) if hasattr(v, "__fspath__") else v) for k, v in result.items()},
                    indent=2,
                )
            )
        else:
            print(f"zip: {result['zip']}")
            print(f"latest: {result['latest']}")
            print(f"files: {result['file_count']}")
            print(f"readme: {result['readme']}")
            print("HITL: deliver zip to accountant yourself — agent does not email.")
        return 0
    return 2


def cmd_validate(args: argparse.Namespace) -> int:
    script = repo_root() / "scripts" / "validate_skills.py"
    import subprocess

    result = subprocess.run([sys.executable, str(script)])
    return result.returncode


def cmd_mcp(args: argparse.Namespace) -> int:
    from nz_startup.mcp_server import run_stdio

    run_stdio()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="nz-startup",
        description="NZ Start-Up in a Box — fleet CLI (HITL: draft/prepare only)",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="Initialise company memory from example")
    init_p.add_argument("company_id")
    init_p.add_argument("--force", action="store_true")
    init_p.set_defaults(func=cmd_init)

    list_p = sub.add_parser("list", help="List company memory IDs")
    list_p.set_defaults(func=cmd_list)

    inst = sub.add_parser("install-skills", help="Install skills into Aether skills path")
    inst.add_argument("--target", help="Destination skills directory")
    inst.add_argument(
        "--mode",
        choices=("copy", "link"),
        default="copy",
        help="copy (default) or symlink",
    )
    inst.set_defaults(func=cmd_install)

    rd = sub.add_parser("rdti", help="RDTI activity log")
    rd_sub = rd.add_subparsers(dest="rdti_cmd", required=True)
    add = rd_sub.add_parser("add", help="Append contemporaneous log row")
    add.add_argument("company_id")
    add.add_argument("--hours", type=float, required=True)
    add.add_argument("--activity", required=True)
    add.add_argument("--uncertainty", required=True, help="Technical uncertainty")
    add.add_argument("--evidence", required=True, help="Commit / timesheet / doc ref")
    add.add_argument("--person", default="Founder")
    add.add_argument("--notes", default="")
    add.add_argument("--date", default=None)
    add.set_defaults(func=cmd_rdti)
    ls = rd_sub.add_parser("list", help="List recent RDTI rows")
    ls.add_argument("company_id")
    ls.add_argument("--limit", type=int, default=20)
    ls.set_defaults(func=cmd_rdti)

    # Pipeline
    pl = sub.add_parser("pipeline", help="CRM-lite pipeline (drafts only)")
    pl_sub = pl.add_subparsers(dest="pipeline_cmd", required=True)
    pl_list = pl_sub.add_parser("list", help="List or summarise deals")
    pl_list.add_argument("company_id")
    pl_list.add_argument("--stage", default=None)
    pl_list.add_argument("--json", action="store_true")
    pl_list.set_defaults(func=cmd_pipeline)
    pl_sum = pl_sub.add_parser("summary", help="Markdown summary")
    pl_sum.add_argument("company_id")
    pl_sum.set_defaults(func=cmd_pipeline)
    pl_add = pl_sub.add_parser("add", help="Add deal")
    pl_add.add_argument("company_id")
    pl_add.add_argument("--account", required=True)
    pl_add.add_argument("--stage", default="lead")
    pl_add.add_argument("--next-step", dest="next_step", default="")
    pl_add.add_argument("--owner", default="Founder")
    pl_add.add_argument("--value", default="")
    pl_add.add_argument("--source", default="")
    pl_add.add_argument("--notes", default="")
    pl_add.set_defaults(func=cmd_pipeline)
    pl_up = pl_sub.add_parser("update", help="Update deal stage/next step")
    pl_up.add_argument("company_id")
    pl_up.add_argument("deal_id")
    pl_up.add_argument("--stage", default=None)
    pl_up.add_argument("--next-step", dest="next_step", default=None)
    pl_up.add_argument("--owner", default=None)
    pl_up.add_argument("--value", default=None)
    pl_up.add_argument("--notes", default=None)
    pl_up.set_defaults(func=cmd_pipeline)

    # Calendar
    cal = sub.add_parser("calendar", help="Compliance calendar + reminders")
    cal_sub = cal.add_subparsers(dest="calendar_cmd", required=True)
    cal_list = cal_sub.add_parser("list")
    cal_list.add_argument("company_id")
    cal_list.add_argument("--status", default=None)
    cal_list.set_defaults(func=cmd_calendar)
    cal_add = cal_sub.add_parser("add")
    cal_add.add_argument("company_id")
    cal_add.add_argument("--item", required=True)
    cal_add.add_argument("--due", required=True, help="ISO date or TBD/Weekly/Ongoing")
    cal_add.add_argument("--owner", default="Founder")
    cal_add.add_argument("--status", default="planned")
    cal_add.add_argument("--category", default="compliance")
    cal_add.add_argument("--recurring", default="")
    cal_add.add_argument("--notes", default="")
    cal_add.set_defaults(func=cmd_calendar)
    cal_up = cal_sub.add_parser("update")
    cal_up.add_argument("company_id")
    cal_up.add_argument("item_id")
    cal_up.add_argument("--due", default=None)
    cal_up.add_argument("--status", default=None)
    cal_up.add_argument("--owner", default=None)
    cal_up.add_argument("--notes", default=None)
    cal_up.add_argument("--item", default=None)
    cal_up.set_defaults(func=cmd_calendar)
    cal_rem = cal_sub.add_parser("remind", help="Upcoming + overdue deadlines")
    cal_rem.add_argument("company_id")
    cal_rem.add_argument("--days", type=int, default=14)
    cal_rem.add_argument("--json", action="store_true")
    cal_rem.set_defaults(func=cmd_calendar)
    cal_seed = cal_sub.add_parser("seed", help="Seed default founder deadlines if empty")
    cal_seed.add_argument("company_id")
    cal_seed.set_defaults(func=cmd_calendar)

    # Grants
    gr = sub.add_parser("grants", help="Grant tracker CSV")
    gr_sub = gr.add_subparsers(dest="grants_cmd", required=True)
    gr_list = gr_sub.add_parser("list")
    gr_list.add_argument("company_id")
    gr_list.add_argument("--status", default=None)
    gr_list.set_defaults(func=cmd_grants)
    gr_add = gr_sub.add_parser("add")
    gr_add.add_argument("company_id")
    gr_add.add_argument("--name", required=True)
    gr_add.add_argument("--funder", default="")
    gr_add.add_argument("--status", default="watch")
    gr_add.add_argument("--fit", default="")
    gr_add.add_argument("--deadline", default="")
    gr_add.add_argument("--amount", default="")
    gr_add.add_argument("--url", default="")
    gr_add.add_argument("--next-action", dest="next_action", default="")
    gr_add.add_argument("--notes", default="")
    gr_add.set_defaults(func=cmd_grants)
    gr_up = gr_sub.add_parser("update")
    gr_up.add_argument("company_id")
    gr_up.add_argument("grant_id")
    gr_up.add_argument("--status", default=None)
    gr_up.add_argument("--fit", default=None)
    gr_up.add_argument("--deadline", default=None)
    gr_up.add_argument("--next-action", dest="next_action", default=None)
    gr_up.add_argument("--notes", default=None)
    gr_up.add_argument("--url", default=None)
    gr_up.set_defaults(func=cmd_grants)
    gr_rank = gr_sub.add_parser("rank", help="Rank open opportunities by fit")
    gr_rank.add_argument("company_id")
    gr_rank.add_argument("--min-fit", type=int, default=0)
    gr_rank.add_argument("--json", action="store_true")
    gr_rank.set_defaults(func=cmd_grants)
    gr_seed = gr_sub.add_parser("seed", help="Seed NZ starter opportunities if empty")
    gr_seed.add_argument("company_id")
    gr_seed.set_defaults(func=cmd_grants)

    wk = sub.add_parser("weekly", help="Generate weekly operating review")
    wk.add_argument("company_id")
    wk.add_argument("--date", default=None)
    wk.set_defaults(func=cmd_weekly)

    nz = sub.add_parser("nzbn", help="Read-only NZBN/name lookup")
    nz.add_argument("query")
    nz.add_argument("--limit", type=int, default=5)
    nz.add_argument("--json", action="store_true")
    nz.set_defaults(func=cmd_nzbn)

    dr = sub.add_parser("draft-outreach", help="Save outreach draft (never sends)")
    dr.add_argument("company_id")
    dr.add_argument("--subject", required=True)
    dr.add_argument("--body", required=True)
    dr.add_argument("--to", default="")
    dr.add_argument("--icp", default="")
    dr.set_defaults(func=cmd_draft_outreach)

    # Xero read-only
    xe = sub.add_parser("xero", help="Xero read-only finance snapshot")
    xe_sub = xe.add_subparsers(dest="xero_cmd", required=True)
    xe_st = xe_sub.add_parser("status", help="Credential mode (no secrets printed)")
    xe_st.set_defaults(func=cmd_xero)
    # status needs no company — fake company_id optional
    xe_st.set_defaults(company_id="_")
    xe_snap = xe_sub.add_parser("snapshot", help="Fetch and write read-only snapshot")
    xe_snap.add_argument("company_id")
    xe_snap.add_argument("--offline", action="store_true", help="Force offline demo")
    xe_snap.add_argument("--json", action="store_true")
    xe_snap.set_defaults(func=cmd_xero)
    xe_ref = xe_sub.add_parser("refresh-token", help="Refresh access token (env only)")
    xe_ref.add_argument(
        "--show-tokens",
        action="store_true",
        help="Print tokens to stdout (dangerous on shared screens)",
    )
    xe_ref.set_defaults(func=cmd_xero, company_id="_")

    # Export reminders
    ex = sub.add_parser("export", help="Export reminders (ICS / digest)")
    ex_sub = ex.add_subparsers(dest="export_cmd", required=True)
    ex_all = ex_sub.add_parser("reminders", help="Write ICS + markdown digest to exports/")
    ex_all.add_argument("company_id")
    ex_all.add_argument("--days", type=int, default=14, help="Digest window")
    ex_all.add_argument("--ics-days", type=int, default=90, help="ICS horizon")
    ex_all.set_defaults(func=cmd_export)
    ex_ics = ex_sub.add_parser("ics", help="ICS only")
    ex_ics.add_argument("company_id")
    ex_ics.add_argument("--days", type=int, default=90)
    ex_ics.add_argument("--stdout", action="store_true")
    ex_ics.set_defaults(func=cmd_export)
    ex_dg = ex_sub.add_parser("digest", help="Markdown digest only")
    ex_dg.add_argument("company_id")
    ex_dg.add_argument("--days", type=int, default=14)
    ex_dg.add_argument("--stdout", action="store_true")
    ex_dg.set_defaults(func=cmd_export)

    # Bank feed
    bk = sub.add_parser("bank", help="Bank feed CSV import + triage")
    bk_sub = bk.add_subparsers(dest="bank_cmd", required=True)
    bk_imp = bk_sub.add_parser("import", help="Import bank CSV export")
    bk_imp.add_argument("company_id")
    bk_imp.add_argument("--file", required=True, help="Path to bank CSV")
    bk_imp.add_argument("--replace", action="store_true", help="Replace existing feed")
    bk_imp.add_argument("--batch", default=None, help="Import batch label")
    bk_imp.set_defaults(func=cmd_bank)
    bk_list = bk_sub.add_parser("list", help="List imported transactions")
    bk_list.add_argument("company_id")
    bk_list.add_argument("--direction", default=None, help="inflow|outflow")
    bk_list.add_argument("--category", default=None)
    bk_list.add_argument("--limit", type=int, default=50)
    bk_list.set_defaults(func=cmd_bank)
    bk_tr = bk_sub.add_parser("triage", help="Category / GST-hint summary")
    bk_tr.add_argument("company_id")
    bk_tr.add_argument("--json", action="store_true")
    bk_tr.set_defaults(func=cmd_bank)

    # GST worksheet
    gt = sub.add_parser("gst", help="GST working papers (not a filing)")
    gt_sub = gt.add_subparsers(dest="gst_cmd", required=True)
    gt_prep = gt_sub.add_parser("prepare", help="Build period worksheet from bank+Xero")
    gt_prep.add_argument("company_id")
    gt_prep.add_argument("--start", required=True, help="Period start YYYY-MM-DD")
    gt_prep.add_argument("--end", required=True, help="Period end YYYY-MM-DD")
    gt_prep.add_argument(
        "--rate",
        type=float,
        default=0.15,
        help="GST rate fraction (default 0.15)",
    )
    gt_prep.add_argument("--label", default=None)
    gt_prep.add_argument("--json", action="store_true")
    gt_prep.set_defaults(func=cmd_gst)

    # Invoices
    inv = sub.add_parser("invoice", help="Invoice PDF/text triage")
    inv_sub = inv.add_subparsers(dest="invoice_cmd", required=True)
    inv_tr = inv_sub.add_parser("triage", help="Triage file or directory of invoices")
    inv_tr.add_argument("company_id")
    inv_tr.add_argument("--path", required=True, help="Invoice file or folder")
    inv_tr.add_argument("--json", action="store_true")
    inv_tr.set_defaults(func=cmd_invoice)
    inv_ls = inv_sub.add_parser("list", help="List triaged invoices")
    inv_ls.add_argument("company_id")
    inv_ls.add_argument("--json", action="store_true")
    inv_ls.set_defaults(func=cmd_invoice)

    # Handoff pack
    ho = sub.add_parser("handoff", help="Accountant handoff pack")
    ho_sub = ho.add_subparsers(dest="handoff_cmd", required=True)
    ho_pack = ho_sub.add_parser("pack", help="Zip working papers for accountant")
    ho_pack.add_argument("company_id")
    ho_pack.add_argument("--label", default="accountant")
    ho_pack.add_argument("--json", action="store_true")
    ho_pack.set_defaults(func=cmd_handoff)

    val = sub.add_parser("validate", help="Validate skill pack")
    val.set_defaults(func=cmd_validate)

    mcp = sub.add_parser("mcp", help="Run MCP stdio server (HITL-safe tools)")
    mcp.set_defaults(func=cmd_mcp)

    return p


def main(argv: list[str] | None = None) -> None:
    """Console entrypoint (raises SystemExit with status code)."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        code = int(args.func(args))
    except (
        FileNotFoundError,
        FileExistsError,
        ValueError,
        PermissionError,
        xero_readonly.XeroError,
    ) as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    raise SystemExit(code)


if __name__ == "__main__":
    main()
