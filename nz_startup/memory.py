"""Company memory operations."""
from __future__ import annotations

import shutil
from pathlib import Path

from nz_startup.audit import append_audit
from nz_startup.paths import company_dir, companies_dir, example_company_dir


SUBDIRS = (
    "weekly",
    "drafts/outreach",
    "drafts/legal",
    "drafts/grants",
    "drafts/content",
    "incorporation-pack",
    "checklists",
)


def init_company(company_id: str, *, force: bool = False) -> Path:
    """Create company memory from the example scaffold."""
    dest = company_dir(company_id)
    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(
            f"Company memory already exists at {dest}. Use force=True to re-seed."
        )
    src = example_company_dir()
    if not src.is_dir():
        raise FileNotFoundError(f"Example company missing: {src}")
    if dest.exists() and force:
        shutil.rmtree(dest)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    for sub in SUBDIRS:
        (dest / sub).mkdir(parents=True, exist_ok=True)
    append_audit(
        dest,
        actor="cli:nz-startup",
        skill="nz-startup-fleet",
        action="init_company_memory",
        summary=f"Initialised company memory for {company_id}",
        tier="platinum",
        artefact_ref=str(dest),
    )
    return dest


def list_companies() -> list[str]:
    root = companies_dir()
    if not root.is_dir():
        return []
    return sorted(
        p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
    )


def _resolve_under_company(company_id: str, relative: str) -> tuple[Path, Path]:
    base = company_dir(company_id).resolve()
    path = (base / relative).resolve()
    try:
        path.relative_to(base)
    except ValueError as e:
        raise PermissionError("Path escapes company memory root") from e
    return base, path


def read_file(company_id: str, relative: str) -> str:
    _, path = _resolve_under_company(company_id, relative)
    if not path.is_file():
        raise FileNotFoundError(relative)
    return path.read_text(encoding="utf-8")


def write_file(
    company_id: str,
    relative: str,
    content: str,
    *,
    actor: str = "agent:memory",
    skill: str = "board-chief-of-staff",
) -> Path:
    base, path = _resolve_under_company(company_id, relative)
    # Refuse secrets-ish filenames
    lowered = relative.lower()
    for bad in (".env", "id_rsa", "service_role", "password", "secret"):
        if bad in lowered:
            raise PermissionError(f"Refusing to write sensitive path fragment: {bad}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    append_audit(
        base,
        actor=actor,
        skill=skill,
        action="write_memory_file",
        summary=f"Wrote {relative} ({len(content)} chars)",
        artefact_ref=relative,
        tier="platinum",
    )
    return path


def append_decision(company_id: str, decision_line: str) -> Path:
    from datetime import date

    base = company_dir(company_id)
    path = base / "decisions.md"
    if not path.exists():
        path.write_text("# Decisions\n\n", encoding="utf-8")
    line = decision_line.strip()
    if not line.startswith("-"):
        line = f"- {date.today().isoformat()} — {line}"
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    append_audit(
        base,
        actor="cli:nz-startup",
        skill="board-chief-of-staff",
        action="append_decision",
        summary=line[:200],
        artefact_ref="decisions.md",
        tier="platinum",
    )
    return path


def ensure_exists(company_id: str) -> Path:
    path = company_dir(company_id)
    if not path.is_dir():
        raise FileNotFoundError(
            f"Unknown company '{company_id}'. Run: nz-startup init {company_id}"
        )
    return path
