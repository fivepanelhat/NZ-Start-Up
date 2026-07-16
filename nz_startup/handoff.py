"""
Accountant handoff pack - zip working papers for human review.

Does not email or upload. Local zip only.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists

# Relative paths under company memory to include when present
HANDOFF_GLOBS = [
 "profile.md",
 "runway.md",
 "finance/xero-snapshot.md",
 "finance/xero-snapshot.json",
 "finance/bank-feed.csv",
 "finance/bank-feed.md",
 "finance/gst/**/*",
 "finance/invoices/invoice-registry.csv",
 "finance/invoices/invoice-registry.md",
 "finance/invoices/triaged/**/*",
 "rdti-log.csv",
 "calendar.csv",
 "calendar.md",
 "exports/deadline-digest-latest.md",
 "exports/deadlines-latest.ics",
 "weekly/*",
]


def _iter_handoff_files(company: Path) -> list[Path]:
 found: set[Path] = set()
 for pattern in HANDOFF_GLOBS:
 for p in company.glob(pattern):
 if p.is_file():
 # skip secrets-ish
 name = p.name.lower()
 if any(x in name for x in ("password", "secret", "token", ".env", "id_rsa")):
 continue
 found.add(p)
 return sorted(found, key=lambda x: str(x))


def build_manifest(company_id: str, files: list[Path], company: Path) -> dict:
 return {
 "product": "nz-startup-in-a-box",
 "company_id": company_id,
 "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "purpose": "Accountant / bookkeeper handoff - working papers only",
 "not_a_tax_filing": True,
 "hitl": "Human reviews and files. Agent does not submit myIR or move money.",
 "file_count": len(files),
 "files": [str(p.relative_to(company)).replace("\\", "/") for p in files],
 "checklist_for_accountant": [
 "Verify bank feed categories and GST treatment",
 "Verify invoice registry against original tax invoices",
 "Reconcile GST worksheet estimates to Xero / IRD records",
 "Confirm period dates before any filing",
 "Do not treat agent confidence scores as legal advice",
 ],
 }


def build_readme(manifest: dict) -> str:
 lines = [
 "# Accountant handoff pack",
 "",
 f"- Company id: `{manifest['company_id']}`",
 f"- Generated: {manifest['generated_at']}",
 f"- Files: {manifest['file_count']}",
 "",
 "## Important",
 "",
 "**NOT A TAX FILING.** Prepared by NZ Start-Up in a Box (agent assist).",
 "You (or the founder's accountant) must verify and file.",
 "",
 "## Suggested review order",
 "",
 "1. `profile.md` / `runway.md`",
 "2. `finance/bank-feed.csv` + triage notes",
 "3. `finance/invoices/invoice-registry.md`",
 "4. `finance/gst/gst-worksheet-latest.md`",
 "5. `finance/xero-snapshot.md` (if present)",
 "6. `rdti-log.csv` (R&D support - separate from GST)",
 "",
 "## Checklist",
 "",
 ]
 for c in manifest.get("checklist_for_accountant") or []:
 lines.append(f"- [ ] {c}")
 lines.extend(["", "## File index", ""])
 for f in manifest.get("files") or []:
 lines.append(f"- `{f}`")
 lines.append("")
 return "\n".join(lines)


def create_handoff_pack(
 company_id: str,
 *,
 label: str | None = None,
) -> dict[str, Path | str | int]:
 company = ensure_exists(company_id)
 files = _iter_handoff_files(company)
 out_dir = company / "handoff"
 out_dir.mkdir(parents=True, exist_ok=True)
 stamp = date.today().isoformat()
 slug = label or "accountant"
 zip_path = out_dir / f"handoff-{slug}-{stamp}.zip"
 latest = out_dir / "handoff-latest.zip"

 manifest = build_manifest(company_id, files, company)
 readme = build_readme(manifest)

 with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
 zf.writestr("HANDOFF_README.md", readme)
 zf.writestr("manifest.json", json.dumps(manifest, indent=2) + "\n")
 for p in files:
 arc = str(p.relative_to(company)).replace("\\", "/")
 zf.write(p, arcname=arc)

 # copy as latest
 latest.write_bytes(zip_path.read_bytes())

 # also leave unzipped readme for convenience
 (out_dir / "HANDOFF_README.md").write_text(readme, encoding="utf-8", newline="\n")
 (out_dir / "manifest-latest.json").write_text(
 json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
 )

 append_audit(
 company,
 actor="agent:finance-clerk",
 skill="finance-clerk",
 action="handoff_pack_create",
 summary=f"Handoff zip {zip_path.name} with {len(files)} files",
 artefact_ref=str(zip_path.relative_to(company)).replace("\\", "/"),
 tier="diamond",
 hitl_required=True,
 hitl_status="pending",
 risk_level="medium",
 )
 return {
 "zip": zip_path,
 "latest": latest,
 "file_count": len(files),
 "manifest": out_dir / "manifest-latest.json",
 "readme": out_dir / "HANDOFF_README.md",
 }
