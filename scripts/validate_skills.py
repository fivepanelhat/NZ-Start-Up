#!/usr/bin/env python3
"""Validate Aether-style skills for NZ Start-Up in a Box."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

REQUIRED_KEYS = ("name", "description", "version")
# Lowercase alnum segments separated by single hyphens
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with --- frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Malformed frontmatter")
    fm_raw = parts[1]
    body = parts[2]
    data: dict[str, str] = {}
    current_key = None
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and current_key == "description":
            data["description"] = (data.get("description", "") + " " + line.strip()).strip()
            continue
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val == ">":
                current_key = key
                data[key] = ""
            else:
                data[key] = val
                current_key = key if key == "description" else None
        elif current_key == "description" and line.startswith("  "):
            data["description"] = (data.get("description", "") + " " + line.strip()).strip()
    return data, body


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as e:
        return [f"{skill_dir.name}: {e}"]

    for key in REQUIRED_KEYS:
        if key not in fm or not fm[key]:
            errors.append(f"{skill_dir.name}: missing frontmatter key '{key}'")

    name = fm.get("name", "")
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: name '{name}' must match directory")
    if name and not NAME_RE.match(name):
        errors.append(f"{skill_dir.name}: invalid name format '{name}'")
    if "--" in name:
        errors.append(f"{skill_dir.name}: consecutive hyphens in name")

    desc = fm.get("description", "")
    if "TODO" in desc.upper():
        errors.append(f"{skill_dir.name}: description contains TODO")
    if len(desc) > 1024:
        errors.append(f"{skill_dir.name}: description too long ({len(desc)})")

    if not body.strip():
        errors.append(f"{skill_dir.name}: empty body")

    # Soft requirements for this product
    lower = text.lower()
    if "requires_hitl" not in lower and skill_dir.name != "market-validator":
        # market-validator may be false but key should exist
        pass
    if "requires_hitl" not in lower:
        errors.append(f"{skill_dir.name}: requires_hitl field recommended/required")

    return errors


def main() -> int:
    if not SKILLS.is_dir():
        print("FAIL: skills/ directory missing", file=sys.stderr)
        return 1
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not dirs:
        print("FAIL: no skills found", file=sys.stderr)
        return 1
    all_errors: list[str] = []
    for d in dirs:
        errs = validate_skill(d)
        if errs:
            all_errors.extend(errs)
        else:
            print(f"OK: {d.name}")
    if all_errors:
        for e in all_errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(f"\nAll {len(dirs)} skills valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
