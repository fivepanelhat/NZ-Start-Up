"""G14/T4 - Skills-pack zip + SHA256 + SBOM provenance helpers."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from nz_startup import __version__
from nz_startup.paths import repo_root


def _sha256_file(path: Path) -> str:
 h = hashlib.sha256()
 with path.open("rb") as f:
 for chunk in iter(lambda: f.read(65536), b""):
 h.update(chunk)
 return h.hexdigest()


def _git_commit() -> str:
 try:
 r = subprocess.run(
 ["git", "rev-parse", "HEAD"],
 cwd=str(repo_root()),
 capture_output=True,
 text=True,
 timeout=10,
 )
 if r.returncode == 0:
 return (r.stdout or "").strip()
 except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
 pass
 return "unknown"


def _sbom_minimal(files: list[Path], root: Path) -> dict[str, Any]:
 """Lightweight CycloneDX-ish component list (no external deps)."""
 components = []
 for p in files:
 rel = str(p.relative_to(root)).replace("\\", "/")
 components.append(
 {
 "type": "file",
 "name": rel,
 "version": __version__,
 "hashes": [{"alg": "SHA-256", "content": _sha256_file(p)}],
 }
 )
 return {
 "bomFormat": "CycloneDX",
 "specVersion": "1.5",
 "version": 1,
 "metadata": {
 "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "component": {
 "type": "application",
 "name": "nz-startup-skills-pack",
 "version": __version__,
 },
 "properties": [
 {"name": "nz.startup.git_commit", "value": _git_commit()},
 {"name": "nz.startup.licence", "value": "dual-proprietary-commercial"},
 ],
 },
 "components": components,
 }


def build_skills_pack(*, out_dir: Path | None = None) -> dict[str, Any]:
 """
 Versioned skills pack for Claude Code / Cowork one-click import.
 T4: SHA256 sidecar + SBOM + provenance commit.
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
 "compliance/standards-mapping.md",
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

 commit = _git_commit()
 manifest = {
 "product": "NZ Start-Up in a Box - skills pack",
 "version": __version__,
 "generated": stamp,
 "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "licence": "dual-proprietary-commercial",
 "owner": "Coastal Alpine Tech Limited",
 "hitl": "Agents inform/draft/prepare/monitor/remind only",
 "file_count": len(files),
 "git_commit": commit,
 "provenance": f"Built from commit {commit} of NZ-Start-Up (local or CI).",
 "install": [
 "Unzip into your agent skills directory, or",
 "pipx install nz-startup-in-a-box (when published), or",
 "pip install -e . && nz-startup install-skills",
 ],
 }

 readme = f"""# NZ Start-Up skills pack v{__version__}

Coastal Alpine Tech Limited - Pre-seed | Taranaki | Aotearoa New Zealand

## HITL

Agents **inform, draft, prepare, monitor, and remind**.
Humans **advise, sign, file, send, and pay**.

## Provenance

- Version: `{__version__}`
- Git commit: `{commit}`
- SHA256: see `*.sha256` sidecar next to this zip

## Install

1. Unzip this pack
2. Copy `skills/*` into your Claude/Aether skills path
3. Optionally: `pip install -e .` from the full repo and run `nz-startup doctor`

## Licence

Dual licence - see LICENSE + LICENSE-COMMERCIAL.md (NZ Copyright Act 1994).
"""

 sbom = _sbom_minimal(files, root)

 with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
 zf.writestr("PACK_README.md", readme)
 zf.writestr("pack-manifest.json", json.dumps(manifest, indent=2) + "\n")
 zf.writestr("sbom.cdx.json", json.dumps(sbom, indent=2) + "\n")
 for p in files:
 arc = str(p.relative_to(root)).replace("\\", "/")
 zf.write(p, arcname=arc)

 latest.write_bytes(zip_path.read_bytes())
 digest = _sha256_file(zip_path)
 sha_path = zip_path.with_suffix(zip_path.suffix + ".sha256")
 sha_path.write_text(f"{digest} {zip_path.name}\n", encoding="utf-8")
 latest_sha = dest / "nz-startup-skills-pack-latest.zip.sha256"
 latest_sha.write_text(f"{digest} nz-startup-skills-pack-latest.zip\n", encoding="utf-8")
 sbom_path = dest / f"nz-startup-skills-pack-v{__version__}-{stamp}.sbom.cdx.json"
 sbom_path.write_text(json.dumps(sbom, indent=2) + "\n", encoding="utf-8")

 return {
 "zip": zip_path,
 "latest": latest,
 "sha256": digest,
 "sha256_file": sha_path,
 "sbom": sbom_path,
 "git_commit": commit,
 "file_count": len(files),
 "version": __version__,
 }
