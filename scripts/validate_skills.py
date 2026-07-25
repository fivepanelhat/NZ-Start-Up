#!/usr/bin/env python3
"""Validate Aether-style skills for NZ Start-Up in a Box.

Accepts both legacy (top-level version) and modern (metadata.version) formats.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

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
        if line.startswith("  ") and current_key in ("description", "related"):
            data[current_key] = (data.get(current_key, "") + " " + line.strip()).strip()
            continue
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val == ">" or val == "|":
                current_key = key
                data[key] = ""
            else:
                data[key] = val
                current_key = key if key in ("description", "related") else None
        elif current_key and line.startswith("  "):
            data[current_key] = (data.get(current_key, "") + " " + line.strip()).strip()
    return data, body


def has_version(fm: dict[str, str], text: str) -> bool:
    if fm.get("version"):
        return True
    # Accept metadata.version
    if "metadata" in text and re.search(r"version:\s*[\"']?\d+\.\d+", text):
        return True
    return False


def has_hitl_signal(text: str) -> bool:
    lower = text.lower()
    return any(
        token in lower
        for token in (
            "requires_hitl",
            "hitl",
            "human action checklist",
            "founder must",
            "human-in-the-loop",
            "approval",
        )
    )


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

    if "name" not in fm or not fm["name"]:
        errors.append(f"{skill_dir.name}: missing frontmatter key 'name'")
    if "description" not in fm or not fm["description"]:
        errors.append(f"{skill_dir.name}: missing frontmatter key 'description'")

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

    if not has_version(fm, text):
        errors.append(f"{skill_dir.name}: version missing (use top-level or metadata.version)")

    if not has_hitl_signal(text):
        errors.append(f"{skill_dir.name}: no HITL signal found (requires_hitl / HITL / founder must / approval)")

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
