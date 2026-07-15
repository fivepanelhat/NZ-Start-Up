"""nz-startup CLI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nz_startup import __version__
from nz_startup import (
    agent_guardrails,
    audit_export,
    backup,
    bank_feed,
    board_pack,
    calendar_ops,
    cohort,
    compliance_gate,
    console,
    demo,
    doctor,
    drafts,
    evals,
    export_reminders,
    grants,
    gst_worksheet,
    handoff,
    invoice_triage,
    memory,
    memory_index,
    model_routing,
    nzbn,
    onboard,
    packaging,
    partner_report,
    pilot_offer,
    pipeline,
    rdti,
    schedule,
    smoke,
    status,
    tasks,
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


def cmd_about(args: argparse.Namespace) -> int:
    from nz_startup import branding

    data = branding.about_dict()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"{data['company']} — {data['stage']}")
        print(f"Product: {data['product']}")
        print(f"Region: {data['region']}")
        print(f"R&D started: {data['rd_start']} · Founded: {data['founding_date']}")
        print(f"Context: {data['founder_context']}")
        print(f"Licence: {data['licence']}")
        print(f"Build tools: {', '.join(data['build_tools'])}")
        print(data["copyright"])
        print("See ABOUT.md and docs/DUAL_LICENCE.md")
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


def cmd_demo(args: argparse.Namespace) -> int:
    if args.demo_cmd == "run":
        report = demo.run_demo(
            args.company,
            partner=args.partner,
            programme=args.programme,
            quick=args.quick,
        )
        if args.json:
            print(json.dumps(report, indent=2, default=str))
        else:
            print(demo.format_demo_markdown(report))
            paths = report.get("paths") or {}
            print("---")
            print(f"latest: {paths.get('latest_md')}")
        return 0
    return 2


def cmd_status(args: argparse.Namespace) -> int:
    st, path = status.write_status(args.company_id)
    if args.json:
        print(json.dumps(st, indent=2))
    else:
        print(status.format_status_markdown(st))
        print(f"---\nwritten: {path}")
    return 0


def cmd_board(args: argparse.Namespace) -> int:
    if args.board_cmd == "pack":
        result = board_pack.create_board_pack(
            args.company_id,
            label=args.label,
            refresh_weekly=not args.no_refresh,
            refresh_status=not args.no_refresh,
        )
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
            print("HITL: deliver board pack yourself — agent does not email.")
        return 0
    return 2


def cmd_smoke(args: argparse.Namespace) -> int:
    report = smoke.run_smoke()
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print(smoke.format_smoke_markdown(report))
    return 0 if report.get("ok") else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    report = doctor.run_doctor()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(doctor.format_doctor_markdown(report))
    return 0 if report.get("ok") else 1


def cmd_harden(args: argparse.Namespace) -> int:
    if args.harden_cmd == "status":
        print(json.dumps(agent_guardrails.guardrails_status(), indent=2))
        return 0
    if args.harden_cmd == "check":
        result = agent_guardrails.classify_risk(
            args.action, context=args.context or "", skill=args.skill or ""
        )
        print(json.dumps(result.as_dict(), indent=2))
        return 0 if result.allowed else 2
    if args.harden_cmd == "policy":
        print(agent_guardrails.skill_policy_block(args.skill or "fleet"))
        return 0
    return 2


def cmd_compliance(args: argparse.Namespace) -> int:
    if args.compliance_cmd in ("check", "report"):
        if args.compliance_cmd == "report" or args.write:
            report, path = compliance_gate.write_compliance_report(args.company)
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                print(compliance_gate.format_compliance_markdown(report))
                print(f"---\nwritten: {path}")
        else:
            report = compliance_gate.run_compliance_check(args.company)
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                print(compliance_gate.format_compliance_markdown(report))
        return 0 if report.get("ok") else 1
    return 2


def cmd_console(args: argparse.Namespace) -> int:
    console.run_console(
        host=args.host,
        port=args.port,
        open_browser=args.open,
        token=getattr(args, "token", None),
    )
    return 0


def cmd_desktop(args: argparse.Namespace) -> int:
    console.run_desktop(port=args.port, token=getattr(args, "token", None))
    return 0


def cmd_tasks(args: argparse.Namespace) -> int:
    if args.tasks_cmd == "add":
        row = tasks.append_task(
            args.company_id,
            title=args.title,
            owner=args.owner or "Founder",
            skill=args.skill or "board-chief-of-staff",
            status=args.status or "todo",
            next_step=args.next_step or "",
            due=args.due or "",
            notes=args.notes or "",
        )
        print(json.dumps(row, indent=2))
        return 0
    if args.tasks_cmd == "list":
        rows = tasks.list_tasks(args.company_id, status=args.status)
        if args.json:
            print(json.dumps(rows, indent=2))
        else:
            for r in rows:
                print(
                    f"{r.get('id')}\t{r.get('status')}\t{r.get('owner')}\t"
                    f"{r.get('title')}\tnext={r.get('next_step')}\tdue={r.get('due')}"
                )
        return 0
    if args.tasks_cmd == "update":
        row = tasks.update_task(
            args.company_id,
            args.task_id,
            status=args.status,
            next_step=args.next_step,
            notes=args.notes,
            owner=args.owner,
        )
        print(json.dumps(row, indent=2))
        return 0
    return 2


def cmd_schedule(args: argparse.Namespace) -> int:
    if args.schedule_cmd == "install":
        result = schedule.install_schedule(force=getattr(args, "force", False))
        print(json.dumps(result, indent=2, default=str))
        # installation may require elevation — non-zero only on hard failure with error key
        if result.get("error") and not result.get("installed"):
            return 1
        return 0
    if args.schedule_cmd == "uninstall":
        print(json.dumps(schedule.uninstall_schedule(), indent=2, default=str))
        return 0
    if args.schedule_cmd == "status":
        print(json.dumps(schedule.schedule_status(), indent=2))
        return 0
    if args.schedule_cmd == "verify":
        result = schedule.verify_schedule()
        print(json.dumps(result, indent=2, default=str))
        return 0 if result.get("ok") else 1
    if args.schedule_cmd == "run":
        # run via relocatable runner (writes heartbeat)
        runner = schedule._runner_script()
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(runner)],
            capture_output=False,
        )
        if getattr(args, "company_id", None):
            # also ensure named company got a pass if list was empty before
            cid = args.company_id
            status.write_status(cid)
            weekly.generate_weekly_review(cid)
            export_reminders.export_all(cid)
            memory_index.write_index(cid)
            print(f"ok: {cid}")
        return int(proc.returncode)
    return 2


def cmd_index(args: argparse.Namespace) -> int:
    if args.index_cmd == "write":
        path = memory_index.write_index(args.company_id)
        print(path)
        return 0
    if args.index_cmd == "compact":
        result = memory_index.compact_memory(args.company_id)
        print(json.dumps(result, indent=2))
        return 0
    return 2


def cmd_eval(args: argparse.Namespace) -> int:
    report = evals.run_evals(
        company_id=args.company_id or "eval-harness",
        live=bool(getattr(args, "live", False)),
        live_provider=getattr(args, "provider", None) or "rubric",
    )
    if args.write:
        path = evals.write_eval_report(report)
        print(f"written: {path}")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(evals.format_eval_markdown(report))
    return 0 if report.get("ok") else 1


def cmd_budget(args: argparse.Namespace) -> int:
    if args.budget_cmd == "show":
        data = model_routing.routing_status(args.company_id)
        print(json.dumps(data, indent=2))
        return 0
    if args.budget_cmd == "set":
        data = model_routing.load_budget(args.company_id)
        if args.tokens is not None:
            data["monthly_token_budget"] = int(args.tokens)
        if args.warn is not None:
            data["warn_fraction"] = float(args.warn)
        if getattr(args, "enforce", None) is not None:
            data["enforce"] = bool(args.enforce)
        model_routing.save_budget(args.company_id, data)
        print(json.dumps(data, indent=2))
        return 0
    if args.budget_cmd == "record":
        data = model_routing.record_usage(
            args.company_id,
            tokens_in=args.tokens_in or 0,
            tokens_out=args.tokens_out or 0,
            skill=args.skill or "",
            model_tier=args.tier or "",
        )
        print(json.dumps(data, indent=2))
        return 0
    return 2


def cmd_pack(args: argparse.Namespace) -> int:
    result = packaging.build_skills_pack()
    out = {k: (str(v) if hasattr(v, "__fspath__") else v) for k, v in result.items()}
    print(json.dumps(out, indent=2))
    return 0


def cmd_backup(args: argparse.Namespace) -> int:
    if args.backup_cmd == "create":
        man = backup.create_backup(
            args.company_id,
            passphrase=args.passphrase,
            out_path=Path(args.out) if args.out else None,
        )
        print(json.dumps(man, indent=2))
        return 0
    if args.backup_cmd == "restore":
        result = backup.restore_backup(
            Path(args.archive),
            passphrase=args.passphrase,
            company_id=args.company,
            force=args.force,
        )
        print(json.dumps(result, indent=2))
        return 0
    return 2


def cmd_audit(args: argparse.Namespace) -> int:
    if args.audit_cmd == "export":
        result = audit_export.export_audit(
            args.company_id,
            format=args.format or "otel-json",
            limit=args.limit or 0,
        )
        print(json.dumps(result, indent=2))
        return 0
    if args.audit_cmd == "rates":
        from nz_startup.audit import cost_rates

        print(json.dumps(cost_rates(), indent=2))
        return 0
    return 2


def cmd_onboard(args: argparse.Namespace) -> int:
    result = onboard.run_onboard(
        args.company_id,
        legal_name=args.legal_name or "",
        trading_name=args.trading_name or "",
        region=args.region or "Aotearoa New Zealand",
        wedge=args.wedge or "",
        icp=args.icp or "",
        force=args.force,
    )
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(onboard.format_onboard_markdown(result))
    return 0


def cmd_pilot(args: argparse.Namespace) -> int:
    if args.pilot_cmd == "offer":
        offer, paths = pilot_offer.prepare_and_write(
            args.company_id,
            customer_name=args.customer,
            pilot_fee_nzd=args.fee,
            term_days=args.days,
            success_criteria=args.criteria or "",
            conversion_price_nzd=args.conversion or "799-999/mo or enterprise quote",
            scope=args.scope or "Sovereign AI pilot — local-first demo + weekly operating cadence",
            champion=args.champion or "",
            start_date=args.start,
        )
        if args.json:
            print(json.dumps({"offer": offer, "paths": {k: str(v) for k, v in paths.items()}}, indent=2))
        else:
            print(pilot_offer.format_offer_markdown(offer))
            print("---")
            for k, p in paths.items():
                print(f"{k}: {p}")
            print("HITL: human sends offer — DRAFT_NOT_SENT")
        return 0
    return 2


def cmd_cohort(args: argparse.Namespace) -> int:
    if args.cohort_cmd == "init":
        cfg = cohort.init_cohort(
            args.cohort_id,
            partner_name=args.partner,
            programme=args.programme or "",
            region=args.region or "Aotearoa New Zealand",
            contact_email=args.email or "",
            seat_quota=args.quota,
            brand_tagline=args.tagline or "",
            force=args.force,
        )
        print(json.dumps(cfg, indent=2) if args.json else cohort.format_cohort_markdown(cfg["cohort_id"]))
        return 0
    if args.cohort_cmd == "add-seat":
        seat = cohort.add_seat(
            args.cohort_id,
            founder_id=args.founder,
            company_id=args.company,
            display_name=args.name or "",
            email=args.email or "",
            force_company_init=args.force,
        )
        print(json.dumps(seat, indent=2))
        return 0
    if args.cohort_cmd == "list":
        if args.cohort_id:
            if args.json:
                print(json.dumps(cohort.list_seats(args.cohort_id), indent=2))
            else:
                print(cohort.format_cohort_markdown(args.cohort_id))
        else:
            print(json.dumps(cohort.list_cohorts(), indent=2))
        return 0
    if args.cohort_cmd == "pack":
        result = cohort.build_white_label_pack(args.cohort_id)
        out = {k: (str(v) if hasattr(v, "__fspath__") else v) for k, v in result.items()}
        print(json.dumps(out, indent=2))
        print("HITL: deliver white-label pack to partner yourself — agent does not email.")
        return 0
    if args.cohort_cmd == "report":
        report, path = partner_report.write_partner_report(
            args.cohort_id, anonymise=args.anonymise
        )
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(partner_report.format_partner_report_markdown(report))
            print(f"---\nwritten: {path}")
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

    ab = sub.add_parser("about", help="Coastal Alpine Tech pre-seed / dual-licence info")
    ab.add_argument("--json", action="store_true")
    ab.set_defaults(func=cmd_about)

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

    # Cohort white-label
    co = sub.add_parser("cohort", help="White-label EDA/accelerator cohorts")
    co_sub = co.add_subparsers(dest="cohort_cmd", required=True)
    co_init = co_sub.add_parser("init", help="Create cohort + brand overlay")
    co_init.add_argument("cohort_id")
    co_init.add_argument("--partner", required=True, help="Partner org name")
    co_init.add_argument("--programme", default="")
    co_init.add_argument("--region", default="Aotearoa New Zealand")
    co_init.add_argument("--email", default="")
    co_init.add_argument("--quota", type=int, default=10)
    co_init.add_argument("--tagline", default="")
    co_init.add_argument("--force", action="store_true")
    co_init.add_argument("--json", action="store_true")
    co_init.set_defaults(func=cmd_cohort)
    co_seat = co_sub.add_parser("add-seat", help="Add founder seat + company memory")
    co_seat.add_argument("cohort_id")
    co_seat.add_argument("--founder", required=True)
    co_seat.add_argument("--company", default=None)
    co_seat.add_argument("--name", default="")
    co_seat.add_argument("--email", default="")
    co_seat.add_argument("--force", action="store_true")
    co_seat.set_defaults(func=cmd_cohort)
    co_list = co_sub.add_parser("list", help="List cohorts or seats")
    co_list.add_argument("cohort_id", nargs="?", default=None)
    co_list.add_argument("--json", action="store_true")
    co_list.set_defaults(func=cmd_cohort)
    co_pack = co_sub.add_parser("pack", help="Build white-label zip (no seat PII)")
    co_pack.add_argument("cohort_id")
    co_pack.set_defaults(func=cmd_cohort)
    co_rep = co_sub.add_parser("report", help="Partner seat readiness report")
    co_rep.add_argument("cohort_id")
    co_rep.add_argument("--anonymise", action="store_true", help="Hide founder/company ids")
    co_rep.add_argument("--json", action="store_true")
    co_rep.set_defaults(func=cmd_cohort)

    # Demo walkthrough
    dm = sub.add_parser("demo", help="EDA / accelerator demo walkthrough")
    dm_sub = dm.add_subparsers(dest="demo_cmd", required=True)
    dm_run = dm_sub.add_parser("run", help="Run demo and write report")
    dm_run.add_argument("--company", default="demo-eda")
    dm_run.add_argument("--partner", default="Venture Taranaki")
    dm_run.add_argument("--programme", default="PowerUp / founder demo")
    dm_run.add_argument("--quick", action="store_true", help="Skip finance deep steps")
    dm_run.add_argument("--json", action="store_true")
    dm_run.set_defaults(func=cmd_demo)

    st = sub.add_parser("status", help="Company readiness dashboard")
    st.add_argument("company_id")
    st.add_argument("--json", action="store_true")
    st.set_defaults(func=cmd_status)

    bd = sub.add_parser("board", help="Mentor/board packs")
    bd_sub = bd.add_subparsers(dest="board_cmd", required=True)
    bd_pack = bd_sub.add_parser("pack", help="Zip mentor/board operating pack")
    bd_pack.add_argument("company_id")
    bd_pack.add_argument("--label", default="mentor")
    bd_pack.add_argument(
        "--no-refresh",
        action="store_true",
        help="Do not regenerate weekly/status before packing",
    )
    bd_pack.add_argument("--json", action="store_true")
    bd_pack.set_defaults(func=cmd_board)

    sm = sub.add_parser("smoke", help="End-to-end smoke test (local sample data)")
    sm.add_argument("--json", action="store_true")
    sm.set_defaults(func=cmd_smoke)

    doc = sub.add_parser("doctor", help="Check install / environment health")
    doc.add_argument("--json", action="store_true")
    doc.set_defaults(func=cmd_doctor)

    hd = sub.add_parser("harden", help="Agent hardening / HITL policy tools")
    hd_sub = hd.add_subparsers(dest="harden_cmd", required=True)
    hd_st = hd_sub.add_parser("status", help="Show guardrails policy snapshot")
    hd_st.set_defaults(func=cmd_harden)
    hd_ck = hd_sub.add_parser("check", help="Classify an action for HITL")
    hd_ck.add_argument("--action", required=True)
    hd_ck.add_argument("--context", default="")
    hd_ck.add_argument("--skill", default="")
    hd_ck.set_defaults(func=cmd_harden)
    hd_pol = hd_sub.add_parser("policy", help="Print policy block for a skill")
    hd_pol.add_argument("--skill", default="fleet")
    hd_pol.set_defaults(func=cmd_harden)

    cp = sub.add_parser("compliance", help="Hardened compliance gate")
    cp_sub = cp.add_subparsers(dest="compliance_cmd", required=True)
    cp_ck = cp_sub.add_parser("check", help="Run compliance control checks")
    cp_ck.add_argument("--company", default=None)
    cp_ck.add_argument("--json", action="store_true")
    cp_ck.add_argument("--write", action="store_true", help="Write report under compliance/reports/")
    cp_ck.set_defaults(func=cmd_compliance)
    cp_rp = cp_sub.add_parser("report", help="Run checks and write report files")
    cp_rp.add_argument("--company", default=None)
    cp_rp.add_argument("--json", action="store_true")
    cp_rp.set_defaults(func=cmd_compliance, write=True)

    con = sub.add_parser("console", help="Localhost Founder Console (session token)")
    con.add_argument("--host", default="127.0.0.1", help="Must be localhost")
    con.add_argument("--port", type=int, default=8765)
    con.add_argument("--open", action="store_true", help="Open system browser")
    con.add_argument("--token", default=None, help="Session token (default: auto-mint)")
    con.set_defaults(func=cmd_console)

    desk = sub.add_parser(
        "desktop",
        help="Desktop-lite window (pywebview if installed, else browser)",
    )
    desk.add_argument("--port", type=int, default=8765)
    desk.add_argument("--token", default=None, help="Session token (default: auto-mint)")
    desk.set_defaults(func=cmd_desktop)

    # G7 tasks
    tk = sub.add_parser("tasks", help="Long-horizon task state (per company)")
    tk_sub = tk.add_subparsers(dest="tasks_cmd", required=True)
    tk_add = tk_sub.add_parser("add", help="Append a task")
    tk_add.add_argument("company_id")
    tk_add.add_argument("--title", required=True)
    tk_add.add_argument("--owner", default="Founder")
    tk_add.add_argument("--skill", default="board-chief-of-staff")
    tk_add.add_argument("--status", default="todo", choices=list(tasks.STATUSES))
    tk_add.add_argument("--next-step", dest="next_step", default="")
    tk_add.add_argument("--due", default="")
    tk_add.add_argument("--notes", default="")
    tk_add.set_defaults(func=cmd_tasks)
    tk_ls = tk_sub.add_parser("list", help="List open tasks")
    tk_ls.add_argument("company_id")
    tk_ls.add_argument("--status", default=None)
    tk_ls.add_argument("--json", action="store_true")
    tk_ls.set_defaults(func=cmd_tasks)
    tk_up = tk_sub.add_parser("update", help="Update task status/next step")
    tk_up.add_argument("company_id")
    tk_up.add_argument("task_id")
    tk_up.add_argument("--status", default=None, choices=list(tasks.STATUSES))
    tk_up.add_argument("--next-step", dest="next_step", default=None)
    tk_up.add_argument("--notes", default=None)
    tk_up.add_argument("--owner", default=None)
    tk_up.set_defaults(func=cmd_tasks)

    # G6 schedule
    sch = sub.add_parser("schedule", help="OS-native weekly cadence (HITL-safe)")
    sch_sub = sch.add_subparsers(dest="schedule_cmd", required=True)
    sch_in = sch_sub.add_parser("install", help="Register OS timer")
    sch_in.add_argument("--force", action="store_true")
    sch_in.set_defaults(func=cmd_schedule)
    sch_un = sch_sub.add_parser("uninstall", help="Remove OS timer")
    sch_un.set_defaults(func=cmd_schedule)
    sch_st = sch_sub.add_parser("status", help="Show schedule artefacts")
    sch_st.set_defaults(func=cmd_schedule)
    sch_vf = sch_sub.add_parser("verify", help="Verify OS task + heartbeat (T5)")
    sch_vf.set_defaults(func=cmd_schedule)
    sch_run = sch_sub.add_parser("run", help="Run cadence now (local)")
    sch_run.add_argument("company_id", nargs="?", default=None)
    sch_run.set_defaults(func=cmd_schedule)

    # G10 index / compact
    ix = sub.add_parser("index", help="Company INDEX.md + memory compaction")
    ix_sub = ix.add_subparsers(dest="index_cmd", required=True)
    ix_w = ix_sub.add_parser("write", help="Refresh INDEX.md")
    ix_w.add_argument("company_id")
    ix_w.set_defaults(func=cmd_index)
    ix_c = ix_sub.add_parser("compact", help="Archive stale weekly + refresh INDEX")
    ix_c.add_argument("company_id")
    ix_c.set_defaults(func=cmd_index)

    # G1/T1 evals
    ev = sub.add_parser("eval", help="Run golden behavioural eval suite")
    ev.add_argument("--company-id", dest="company_id", default="eval-harness")
    ev.add_argument("--json", action="store_true")
    ev.add_argument("--write", action="store_true", help="Write evals/reports/")
    ev.add_argument(
        "--live",
        action="store_true",
        help="T1 opt-in behavioural lane (rubric / LLM-as-judge ready)",
    )
    ev.add_argument(
        "--provider",
        default="rubric",
        help="Live judge provider: rubric (default) or future openai|xai",
    )
    ev.set_defaults(func=cmd_eval)

    # G9/T6 budget / routing
    bg = sub.add_parser("budget", help="Model tier routing + monthly token budget")
    bg_sub = bg.add_subparsers(dest="budget_cmd", required=True)
    bg_sh = bg_sub.add_parser("show", help="Show routing map + company budget")
    bg_sh.add_argument("company_id", nargs="?", default=None)
    bg_sh.set_defaults(func=cmd_budget)
    bg_set = bg_sub.add_parser("set", help="Set monthly token budget")
    bg_set.add_argument("company_id")
    bg_set.add_argument("--tokens", type=int, default=None)
    bg_set.add_argument("--warn", type=float, default=None, help="Warn fraction 0-1")
    bg_set.add_argument(
        "--enforce",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="T6 hard cap: refuse frontier when exhausted",
    )
    bg_set.set_defaults(func=cmd_budget)
    bg_rec = bg_sub.add_parser("record", help="Record token usage against budget")
    bg_rec.add_argument("company_id")
    bg_rec.add_argument("--tokens-in", dest="tokens_in", type=int, default=0)
    bg_rec.add_argument("--tokens-out", dest="tokens_out", type=int, default=0)
    bg_rec.add_argument("--skill", default="")
    bg_rec.add_argument("--tier", default="", choices=["", "light", "standard", "frontier"])
    bg_rec.set_defaults(func=cmd_budget)

    # G14/T4 pack
    pk = sub.add_parser("pack", help="Build versioned skills-pack zip + SHA256 + SBOM")
    pk.set_defaults(func=cmd_pack)

    # T7 backup
    bk = sub.add_parser("backup", help="Encrypted local company backup (T7)")
    bk_sub = bk.add_subparsers(dest="backup_cmd", required=True)
    bk_c = bk_sub.add_parser("create", help="Create encrypted .nzbak archive")
    bk_c.add_argument("company_id")
    bk_c.add_argument("--passphrase", required=True)
    bk_c.add_argument("--out", default=None, help="Output path")
    bk_c.set_defaults(func=cmd_backup)
    bk_r = bk_sub.add_parser("restore", help="Restore encrypted archive")
    bk_r.add_argument("archive")
    bk_r.add_argument("--passphrase", required=True)
    bk_r.add_argument("--company", default=None)
    bk_r.add_argument("--force", action="store_true")
    bk_r.set_defaults(func=cmd_backup)

    # T8 audit export
    au = sub.add_parser("audit", help="Audit log export / cost rates")
    au_sub = au.add_subparsers(dest="audit_cmd", required=True)
    au_ex = au_sub.add_parser("export", help="Export OTel-GenAI-shaped JSON")
    au_ex.add_argument("company_id")
    au_ex.add_argument(
        "--format",
        default="otel-json",
        choices=("otel-json", "jsonl"),
    )
    au_ex.add_argument("--limit", type=int, default=0)
    au_ex.set_defaults(func=cmd_audit)
    au_rt = au_sub.add_parser("rates", help="Show NZD cost rate table + verified date")
    au_rt.set_defaults(func=cmd_audit)

    ob = sub.add_parser("onboard", help="Founder first-hour onboarding wizard")
    ob.add_argument("company_id")
    ob.add_argument("--legal-name", dest="legal_name", default="")
    ob.add_argument("--trading-name", dest="trading_name", default="")
    ob.add_argument("--region", default="Aotearoa New Zealand")
    ob.add_argument("--wedge", default="")
    ob.add_argument("--icp", default="")
    ob.add_argument("--force", action="store_true")
    ob.add_argument("--json", action="store_true")
    ob.set_defaults(func=cmd_onboard)

    pi = sub.add_parser("pilot", help="Paid pilot commercial packs")
    pi_sub = pi.add_subparsers(dest="pilot_cmd", required=True)
    pi_off = pi_sub.add_parser("offer", help="Draft paid pilot offer pack")
    pi_off.add_argument("company_id")
    pi_off.add_argument("--customer", required=True)
    pi_off.add_argument("--fee", default="1500", help="Pilot fee NZD")
    pi_off.add_argument("--days", type=int, default=90)
    pi_off.add_argument("--start", default=None, help="Start date YYYY-MM-DD")
    pi_off.add_argument("--champion", default="")
    pi_off.add_argument("--criteria", default="")
    pi_off.add_argument("--conversion", default="799-999/mo or enterprise quote")
    pi_off.add_argument("--scope", default="")
    pi_off.add_argument("--json", action="store_true")
    pi_off.set_defaults(func=cmd_pilot)

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
