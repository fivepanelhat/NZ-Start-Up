"""
White-label cohort packaging for EDAs / accelerators / incubators.

Local multi-seat structure under cohorts/<id>/. Does not host SaaS tenancy.
Autonomy ceilings unchanged: seats still draft/prepare only.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from nz_startup import __version__, memory
from nz_startup.audit import append_audit
from nz_startup.paths import repo_root, skills_dir

COHORT_SCHEMA_VERSION = 1


def cohorts_root() -> Path:
    root = repo_root() / "cohorts"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _safe_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    if not cleaned:
        raise ValueError("id must contain letters or numbers")
    return cleaned


def cohort_dir(cohort_id: str) -> Path:
    return cohorts_root() / _safe_id(cohort_id)


def config_path(cohort_id: str) -> Path:
    return cohort_dir(cohort_id) / "cohort.json"


def load_config(cohort_id: str) -> dict[str, Any]:
    path = config_path(cohort_id)
    if not path.is_file():
        raise FileNotFoundError(f"Unknown cohort '{cohort_id}'. Run: nz-startup cohort init …")
    return json.loads(path.read_text(encoding="utf-8"))


def save_config(config: dict[str, Any]) -> Path:
    cid = config["cohort_id"]
    path = config_path(cid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return path


def init_cohort(
    cohort_id: str,
    *,
    partner_name: str,
    partner_slug: str | None = None,
    contact_email: str = "",
    region: str = "Aotearoa New Zealand",
    programme: str = "",
    seat_quota: int = 10,
    brand_tagline: str = "",
    support_url: str = "",
    force: bool = False,
) -> dict[str, Any]:
    cid = _safe_id(cohort_id)
    cdir = cohort_dir(cid)
    if cdir.exists() and any(cdir.iterdir()) and not force:
        raise FileExistsError(f"Cohort already exists: {cdir}. Use force=True to re-init.")
    if force and cdir.exists():
        shutil.rmtree(cdir)
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "seats").mkdir(exist_ok=True)
    (cdir / "brand").mkdir(exist_ok=True)
    (cdir / "exports").mkdir(exist_ok=True)

    partner_slug = _safe_id(partner_slug or partner_name)
    config: dict[str, Any] = {
        "schema_version": COHORT_SCHEMA_VERSION,
        "cohort_id": cid,
        "partner_name": partner_name.strip(),
        "partner_slug": partner_slug,
        "programme": programme.strip() or "Founder cohort",
        "region": region.strip(),
        "contact_email": contact_email.strip(),
        "support_url": support_url.strip(),
        "seat_quota": int(seat_quota),
        "seats": [],
        "brand": {
            "product_name": f"{partner_name.strip()} Start-Up Box",
            "tagline": brand_tagline.strip()
            or "NZ founder operating system — draft and prepare, humans decide",
            "powered_by": "NZ Start-Up in a Box · Coastal Alpine Tech · Aether",
            "hitl_slogan": (
                "Agents inform, draft, prepare, monitor, and remind. "
                "Humans advise, sign, file, send, and pay."
            ),
            "disclaimer": (
                "Not legal, financial, tax, or cultural advice. "
                "White-label packaging does not remove NZ legal ceilings."
            ),
        },
        "pricing_note": {
            "model": "per-seat or per-cohort white-label",
            "indicative": "Founder ~NZ$49 · Active ~NZ$149 · Accelerator seat ~NZ$399 · custom white-label",
            "token_burn_note": "Default agents to on-demand + weekly cadence; always-on autonomy is the cost trap",
        },
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "product_version": __version__,
    }
    save_config(config)
    _write_brand_files(config)
    _write_partner_readme(config)
    return config


def _write_brand_files(config: dict[str, Any]) -> None:
    brand = config["brand"]
    cdir = cohort_dir(config["cohort_id"])
    brand_dir = cdir / "brand"
    (brand_dir / "BRAND.md").write_text(
        "\n".join(
            [
                f"# {brand['product_name']}",
                "",
                f"> {brand['tagline']}",
                "",
                f"**Partner:** {config['partner_name']}",
                f"**Programme:** {config['programme']}",
                f"**Region:** {config['region']}",
                "",
                "## Autonomy (non-negotiable)",
                "",
                brand["hitl_slogan"],
                "",
                "## Disclaimer",
                "",
                brand["disclaimer"],
                "",
                f"_Powered by {brand['powered_by']}_",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    (brand_dir / "welcome.md").write_text(
        "\n".join(
            [
                f"# Nau mai — {brand['product_name']}",
                "",
                f"You are on the **{config['programme']}** programme with "
                f"**{config['partner_name']}**.",
                "",
                "This seat gives you a local NZ founder agent fleet:",
                "",
                "1. Formation, compliance, grants/RDTI, market, GTM, content",
                "2. Finance bank/GST working papers, invoice triage, accountant handoff",
                "3. Weekly board review — the product experience",
                "",
                "## First 15 minutes",
                "",
                "```bash",
                "nz-startup init <your-company-id>",
                "nz-startup weekly <your-company-id>",
                "nz-startup pipeline add <your-company-id> --account \"First target\" --stage discovery",
                "```",
                "",
                "## Hard rules",
                "",
                "- Do **not** let agents send cold email, file IRD/Companies Office, or move money",
                "- Confirm legal/tax with qualified humans before relying on drafts",
                "",
                brand["disclaimer"],
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )


def _write_partner_readme(config: dict[str, Any]) -> None:
    cdir = cohort_dir(config["cohort_id"])
    (cdir / "PARTNER_README.md").write_text(
        "\n".join(
            [
                f"# Partner ops — {config['partner_name']}",
                "",
                f"Cohort id: `{config['cohort_id']}`",
                f"Seat quota: {config['seat_quota']}",
                f"Product version: {config.get('product_version')}",
                "",
                "## Commands",
                "",
                "```bash",
                f"nz-startup cohort add-seat {config['cohort_id']} --founder my-founder --company my-co",
                f"nz-startup cohort list {config['cohort_id']}",
                f"nz-startup cohort pack {config['cohort_id']}",
                f"nz-startup demo run --company <seat-company> --partner \"{config['partner_name']}\"",
                "```",
                "",
                "## White-label thesis",
                "",
                "Sell **per-cohort / per-seat** capacity to EDAs and accelerators —",
                "\"Nick, but scalable\" — without multi-tenant SaaS until funded.",
                "",
                "## Compliance",
                "",
                "- Privacy Act 2020: prefer local seat data on founder machines",
                "- UEM Act: outreach drafts only",
                "- No legal/financial advice by agents",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )


def add_seat(
    cohort_id: str,
    *,
    founder_id: str,
    company_id: str | None = None,
    display_name: str = "",
    email: str = "",
    force_company_init: bool = False,
) -> dict[str, Any]:
    config = load_config(cohort_id)
    fid = _safe_id(founder_id)
    company = _safe_id(company_id or f"{config['cohort_id']}-{fid}")
    seats = config.get("seats") or []
    if any(s.get("founder_id") == fid for s in seats):
        raise FileExistsError(f"Seat for founder '{fid}' already exists in cohort")
    if len(seats) >= int(config.get("seat_quota") or 0):
        raise ValueError(
            f"Seat quota reached ({config['seat_quota']}). Increase quota in cohort.json"
        )

    # Init company memory for the seat
    try:
        memory.init_company(company, force=force_company_init)
    except FileExistsError:
        if force_company_init:
            memory.init_company(company, force=True)
        # else reuse existing company memory

    seat = {
        "founder_id": fid,
        "company_id": company,
        "display_name": display_name.strip() or fid,
        "email": email.strip(),
        "status": "active",
        "added_at": date.today().isoformat(),
    }
    seats.append(seat)
    config["seats"] = seats
    save_config(config)

    # Per-seat welcome
    seat_dir = cohort_dir(cohort_id) / "seats" / fid
    seat_dir.mkdir(parents=True, exist_ok=True)
    (seat_dir / "seat.json").write_text(json.dumps(seat, indent=2) + "\n", encoding="utf-8")
    brand = config["brand"]
    (seat_dir / "WELCOME.md").write_text(
        f"# Seat: {seat['display_name']}\n\n"
        f"- Company memory id: `{company}`\n"
        f"- Cohort: `{config['cohort_id']}` ({config['partner_name']})\n"
        f"- Product: {brand['product_name']}\n\n"
        f"Run: `nz-startup weekly {company}`\n\n"
        f"{brand['hitl_slogan']}\n",
        encoding="utf-8",
        newline="\n",
    )
    return seat


def list_cohorts() -> list[dict[str, Any]]:
    out = []
    for p in sorted(cohorts_root().iterdir()):
        if p.is_dir() and (p / "cohort.json").is_file():
            cfg = json.loads((p / "cohort.json").read_text(encoding="utf-8"))
            out.append(
                {
                    "cohort_id": cfg.get("cohort_id"),
                    "partner_name": cfg.get("partner_name"),
                    "seats": len(cfg.get("seats") or []),
                    "seat_quota": cfg.get("seat_quota"),
                    "programme": cfg.get("programme"),
                }
            )
    return out


def list_seats(cohort_id: str) -> list[dict[str, Any]]:
    return list(load_config(cohort_id).get("seats") or [])


def format_cohort_markdown(cohort_id: str) -> str:
    cfg = load_config(cohort_id)
    seats = cfg.get("seats") or []
    lines = [
        f"# Cohort — {cfg.get('partner_name')}",
        "",
        f"- Id: `{cfg.get('cohort_id')}`",
        f"- Programme: {cfg.get('programme')}",
        f"- Seats: {len(seats)} / {cfg.get('seat_quota')}",
        f"- Product: {cfg.get('brand', {}).get('product_name')}",
        "",
        "## Seats",
        "",
    ]
    if not seats:
        lines.append("_No seats yet_")
    for s in seats:
        lines.append(
            f"- `{s.get('founder_id')}` → company `{s.get('company_id')}` "
            f"({s.get('status')}) — {s.get('display_name')}"
        )
    lines.extend(
        [
            "",
            "## HITL",
            "",
            cfg.get("brand", {}).get("hitl_slogan", ""),
            "",
            cfg.get("brand", {}).get("disclaimer", ""),
            "",
        ]
    )
    return "\n".join(lines)


def build_white_label_pack(cohort_id: str) -> dict[str, Path | int | str]:
    """
    Zip a white-label distribution pack for the partner:
    brand files, partner readme, skills pointer, install notes, mcp sample.
    Does not include live founder PII company memories.
    """
    cfg = load_config(cohort_id)
    cdir = cohort_dir(cohort_id)
    exports = cdir / "exports"
    exports.mkdir(exist_ok=True)
    stamp = date.today().isoformat()
    zip_path = exports / f"white-label-{cfg['cohort_id']}-{stamp}.zip"
    latest = exports / "white-label-latest.zip"

    # Assemble staging
    staging = cdir / ".pack-staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()

    (staging / "README.md").write_text(
        _pack_readme(cfg), encoding="utf-8", newline="\n"
    )
    (staging / "cohort.json").write_text(
        json.dumps(
            {
                k: cfg[k]
                for k in cfg
                if k != "seats"  # no seat PII in distribution pack
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    shutil.copytree(cdir / "brand", staging / "brand")
    shutil.copy2(cdir / "PARTNER_README.md", staging / "PARTNER_README.md")

    # skills catalog pointer (not full copy to keep pack small — include list)
    skill_names = sorted(p.name for p in skills_dir().iterdir() if p.is_dir())
    (staging / "SKILLS.md").write_text(
        "# Included fleet skills\n\n"
        + "\n".join(f"- `{n}`" for n in skill_names)
        + "\n\nInstall full product from GitHub, then:\n\n"
        "```bash\nnz-startup install-skills\n```\n",
        encoding="utf-8",
        newline="\n",
    )
    (staging / "mcp.sample.json").write_text(
        json.dumps(
            {
                "mcpServers": {
                    cfg["partner_slug"] + "-startup-box": {
                        "command": "python",
                        "args": ["-m", "nz_startup", "mcp"],
                        "env": {
                            "NZ_STARTUP_ROOT": ".",
                        },
                    }
                }
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (staging / "INSTALL.md").write_text(
        "\n".join(
            [
                f"# Install — {cfg['brand']['product_name']}",
                "",
                "1. `git clone https://github.com/fivepanelhat/NZ-Start-Up.git`",
                "2. `pip install -e \".[all]\"`",
                "3. `nz-startup install-skills`",
                f"4. `nz-startup cohort init {cfg['cohort_id']} --partner \"{cfg['partner_name']}\"` "
                "(or use this pack's cohort.json as reference)",
                "5. Add seats with `nz-startup cohort add-seat …`",
                "6. Run `nz-startup demo run --company <seat-company>` for walkthrough",
                "",
                "## Legal",
                "",
                cfg["brand"]["disclaimer"],
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for p in staging.rglob("*"):
            if p.is_file():
                zf.write(p, arcname=str(p.relative_to(staging)).replace("\\", "/"))
    latest.write_bytes(zip_path.read_bytes())
    shutil.rmtree(staging)

    return {
        "zip": zip_path,
        "latest": latest,
        "cohort_id": cfg["cohort_id"],
        "partner_name": cfg["partner_name"],
        "seats_excluded": len(cfg.get("seats") or []),
    }


def _pack_readme(cfg: dict[str, Any]) -> str:
    brand = cfg["brand"]
    return "\n".join(
        [
            f"# {brand['product_name']}",
            "",
            f"> {brand['tagline']}",
            "",
            f"White-label pack for **{cfg['partner_name']}** · `{cfg['cohort_id']}`",
            "",
            "## What's inside",
            "",
            "- Brand overlay + founder welcome",
            "- Partner ops readme",
            "- MCP sample config",
            "- Skills inventory + install path",
            "- Cohort config **without seat PII**",
            "",
            "## What this is not",
            "",
            "- Not multi-tenant hosted SaaS",
            "- Not autonomous filing/sending/paying",
            "- Not legal or financial advice",
            "",
            brand["hitl_slogan"],
            "",
            f"_Pack generated for product v{cfg.get('product_version', __version__)}_",
            f"_Powered by {brand['powered_by']}_",
            "",
        ]
    )
