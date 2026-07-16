"""Resolve package and company-memory paths."""
from __future__ import annotations

import os
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def repo_root() -> Path:
 env = os.environ.get("NZ_STARTUP_ROOT")
 if env:
 return Path(env).expanduser().resolve()
 return REPO_ROOT


def skills_dir() -> Path:
 return repo_root() / "skills"


def templates_dir() -> Path:
 return repo_root() / "templates"


def memory_root() -> Path:
 env = os.environ.get("NZ_STARTUP_MEMORY")
 if env:
 return Path(env).expanduser().resolve()
 return repo_root() / "memory"


def companies_dir() -> Path:
 return memory_root() / "companies"


def example_company_dir() -> Path:
 return memory_root() / "example-company"


def company_dir(company_id: str) -> Path:
 safe = _safe_id(company_id)
 return companies_dir() / safe


def _safe_id(company_id: str) -> str:
 cleaned = "".join(c if c.isalnum() or c in "-_" else "-" for c in company_id.strip())
 cleaned = cleaned.strip("-_").lower()
 if not cleaned:
 raise ValueError("company_id must contain letters or numbers")
 return cleaned
