"""Smoke tests for NZ Start-Up in a Box skills pack."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED = {
    "cat-architectural-standards",
    "nz-startup-fleet",
    "board-chief-of-staff",
    "formation-officer",
    "compliance-registrar",
    "grants-rdti-clerk",
    "market-validator",
    "gtm-pipeline-rep",
    "content-comms-officer",
    "finance-clerk",
    "funding-analyst",
    "legal-document-assistant",
}


def test_expected_skills_present():
    found = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    assert EXPECTED.issubset(found), f"Missing: {EXPECTED - found}"


def test_validate_skills_script_passes():
    script = ROOT / "scripts" / "validate_skills.py"
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_hitl_matrix_exists():
    assert (ROOT / "compliance" / "hitl-matrix.md").is_file()


def test_example_rdti_log_csv():
    path = ROOT / "memory" / "example-company" / "rdti-log.csv"
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows, "example rdti log should have at least one row"
    assert "hours" in rows[0]


def test_readme_mentions_standards():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Gold" in text and "Diamond" in text and "Platinum" in text


def test_each_skill_has_changelog():
    for name in EXPECTED:
        path = SKILLS / name / "references" / "CHANGELOG.md"
        assert path.is_file(), f"missing changelog for {name}"
