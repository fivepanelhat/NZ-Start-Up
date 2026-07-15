"""G14 — Skills-pack zip + pipx-friendly distribution helpers."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from nz_startup import __version__
from nz_startup.paths import repo_root


def build_skills_pack(*, out_dir: Path | None = None) -> dict[str, Any]:
    """
    Versioned skills pack for Claude Code / Cowork one-click import.
    Includes skills/, standards snippets, AGENTS.md, dual-licence notice.
    """
    root = repo_root()
    dest = out_dir or (root / "dist")
    dest.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    name = f"nz-startup-skills-pack-v{__version__}-{stamp}.zip"
    zip_path = dest / name
    latest = dest / "nz-startup-skills-pack-latest.zip"

    include_globs = [
        "skills/**/*",
        "standards/**/*",
        "AGENTS.md",
        "LICENSE",
        "LICENSE-COMMERCIAL.md",
        "NOTICE",
        "COMPLIANCE.md",
        "compliance/hitl-matrix.md",
        "compliance/legal-boundaries-nz.md",
        "docs/STANDARDS.md",
        "docs/GETTING_STARTED.md",
        "mcp.json",
        "knowledge/**/*",
    ]

    files: list[Path] = []
    for pattern in include_globs:
        for p in root.glob(pattern):
            if p.is_file() and "__pycache__" not in p.parts:
                files.append(p)

    manifest = {
        "product": "NZ Start-Up in a Box — skills pack",
        "version": __version__,
        "generated": stamp,
        "licence": "dual-proprietary-commercial",
        "owner": "Coastal Alpine Tech Limited",
        "hitl": "Agents inform/draft/prepare/monitor/remind only",
        "file_count": len(files),
        "install": [
            "Unzip into your agent skills directory, or",
            "pipx install nz-startup-in-a-box (when published), or",
            "pip install -e . && nz-startup install-skills",
        ],
    }

    readme = f"""# NZ Start-Up skills pack v{__version__}

Coastal Alpine Tech Limited — Pre-seed · Taranaki · Aotearoa New Zealand

## HITL

Agents **inform, draft, prepare, monitor, and remind**.
Humans **advise, sign, file, send, and pay**.

## Install

1. Unzip this pack
2. Copy `skills/*` into your Claude/Aether skills path
3. Optionally: `pip install -e .` from the full repo and run `nz-startup doctor`

## Licence

Dual licence — see LICENSE + LICENSE-COMMERCIAL.md (NZ Copyright Act 1994).
"""

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr("PACK_README.md", readme)
        zf.writestr("pack-manifest.json", __import__("json").dumps(manifest, indent=2) + "\n")
        for p in files:
            arc = str(p.relative_to(root)).replace("\\", "/")
            zf.write(p, arcname=arc)

    latest.write_bytes(zip_path.read_bytes())
    return {
        "zip": zip_path,
        "latest": latest,
        "file_count": len(files),
        "version": __version__,
    }
