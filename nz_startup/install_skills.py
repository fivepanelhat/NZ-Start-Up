"""Install fleet skills into Aether or a custom skills directory."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from nz_startup.paths import skills_dir


def default_aether_skills() -> Path:
 env = os.environ.get("AETHER_SKILLS_PATH")
 if env:
 return Path(env).expanduser().resolve()
 return Path.home() / ".aether" / "skills"


def install_skills(
 target: Path | None = None,
 *,
 mode: str = "copy",
) -> list[str]:
 """
 mode: 'copy' | 'link'
 Returns list of installed skill names.
 """
 src_root = skills_dir()
 if not src_root.is_dir():
 raise FileNotFoundError(f"skills directory missing: {src_root}")
 dest_root = target or default_aether_skills()
 dest_root.mkdir(parents=True, exist_ok=True)
 installed: list[str] = []
 for skill in sorted(p for p in src_root.iterdir() if p.is_dir()):
 dest = dest_root / skill.name
 if dest.exists() or dest.is_symlink():
 if dest.is_dir() and not dest.is_symlink():
 shutil.rmtree(dest)
 else:
 dest.unlink()
 if mode == "link":
 try:
 dest.symlink_to(skill.resolve(), target_is_directory=True)
 except OSError:
 # Windows without symlink privilege - fall back to copy
 shutil.copytree(skill, dest)
 else:
 shutil.copytree(skill, dest)
 installed.append(skill.name)
 return installed
