#!/usr/bin/env python3
"""
Automated tests for the four new NZ-Start-Up skills added 2026-07-20.

These tests run against the skills/ directory in the repository root.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

NEW_SKILLS = [
    "nz-company-formation",
    "venture-taranaki-engagement",
    "nz-startup-partnership",
    "nz-startup-launch-sequence",
]

REQUIRED_FRONTMATTER = ("name", "description")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with --- frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Malformed frontmatter")
    fm_raw = parts[1]
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
    return data


class TestNewSkillsExist:
    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_skill_directory_exists(self, skill_name: str):
        skill_dir = SKILLS_DIR / skill_name
        assert skill_dir.is_dir(), f"Missing skill directory: {skill_dir}"

    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_skill_md_exists(self, skill_name: str):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        assert skill_md.is_file(), f"Missing SKILL.md for {skill_name}"


class TestNewSkillsFrontmatter:
    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_required_keys_present(self, skill_name: str):
        text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        for key in REQUIRED_FRONTMATTER:
            assert key in fm and fm[key], f"{skill_name}: missing or empty '{key}'"

    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_name_matches_directory(self, skill_name: str):
        text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        assert fm.get("name") == skill_name

    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_name_format(self, skill_name: str):
        assert NAME_RE.match(skill_name), f"Invalid name format: {skill_name}"

    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_description_length(self, skill_name: str):
        text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        desc = fm.get("description", "")
        assert 20 < len(desc) <= 1024, f"{skill_name}: description length {len(desc)}"

    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_hitl_signal_present(self, skill_name: str):
        text = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8").lower()
        assert any(t in text for t in ("hitl", "founder must", "human action", "approval")), (
            f"{skill_name}: no HITL signal found"
        )

    @pytest.mark.parametrize("skill_name", NEW_SKILLS)
    def test_changelog_exists(self, skill_name: str):
        changelog = SKILLS_DIR / skill_name / "references" / "CHANGELOG.md"
        assert changelog.is_file(), f"{skill_name}: missing references/CHANGELOG.md"


class TestNewSkillsContent:
    """Light content smoke tests — ensure the skills actually contain the expected guidance."""

    def test_company_formation_mentions_realme(self):
        text = (SKILLS_DIR / "nz-company-formation" / "SKILL.md").read_text(encoding="utf-8").lower()
        assert "realme" in text
        assert "founder" in text

    def test_venture_taranaki_mentions_nick_and_scaleup(self):
        text = (SKILLS_DIR / "venture-taranaki-engagement" / "SKILL.md").read_text(encoding="utf-8").lower()
        assert "nick" in text
        assert "scaleup" in text or "scale-up" in text
        assert "powerup" in text or "power-up" in text

    def test_partnership_mentions_loi_and_te_mana(self):
        text = (SKILLS_DIR / "nz-startup-partnership" / "SKILL.md").read_text(encoding="utf-8").lower()
        assert "loi" in text or "letter of intent" in text
        assert "te mana raraunga" in text or "data-sovereignty" in text or "data sovereignty" in text

    def test_launch_sequence_mentions_30_60_90(self):
        text = (SKILLS_DIR / "nz-startup-launch-sequence" / "SKILL.md").read_text(encoding="utf-8").lower()
        assert "30" in text and "60" in text and "90" in text
        assert "board pack" in text or "weekly" in text


class TestValidateSkillsScript:
    """Run the repo validator and ensure the new skills pass."""

    def test_repo_validator_passes_new_skills(self):
        validator = ROOT / "scripts" / "validate_skills.py"
        assert validator.exists(), "scripts/validate_skills.py missing"
        result = subprocess.run(
            [sys.executable, str(validator)],
            capture_output=True, text=True, cwd=ROOT
        )
        for skill in NEW_SKILLS:
            assert f"OK: {skill}" in result.stdout, (
                f"Validator did not accept {skill}:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )
        assert result.returncode == 0, result.stderr
