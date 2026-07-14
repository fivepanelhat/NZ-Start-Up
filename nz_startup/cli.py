"""nz-startup CLI."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nz_startup import __version__
from nz_startup import drafts, memory, nzbn, rdti, weekly
from nz_startup.install_skills import default_aether_skills, install_skills
from nz_startup.paths import repo_root


def cmd_init(args: argparse.Namespace) -> int:
    path = memory.init_company(args.company_id, force=args.force)
    print(f"Initialised company memory: {path}")
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
    except (FileNotFoundError, FileExistsError, ValueError, PermissionError) as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    raise SystemExit(code)


if __name__ == "__main__":
    main()
