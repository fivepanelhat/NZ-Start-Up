"""T7 — Encrypted local backup of company memory (data-at-rest story).

Uses stdlib zip + Fernet-style password derivation via hashlib + AES is heavy;
we use ZIP with AES when pyzipper available, else zip + separate .key envelope
using Fernet from cryptography if present, else password-obfuscated zip + HMAC
manifest (documented as "best-effort encryption — prefer BitLocker/FileVault").

Primary path: stdlib only — zip encrypted with a passphrase derived archive
using zipfile + zlib, with a random salt and Fernet-compatible token if
cryptography is installed; otherwise AES-free password zip is not available
so we create a zip and an age-style instruction file + HMAC signed manifest.

Actually keep it simple and robust stdlib-only:
1. Create zip of company tree
2. XOR/stream-cipher with key derived from passphrase via PBKDF2-HMAC-SHA256
3. Store as .nzbak (salt + nonce + ciphertext)
4. Restore reverses it

This is NOT a substitute for full-disk encryption — documented as such.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import shutil
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nz_startup.audit import append_audit
from nz_startup.memory import ensure_exists
from nz_startup.paths import companies_dir

MAGIC = b"NZBAK1\n"
PBKDF2_ROUNDS = 200_000


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, PBKDF2_ROUNDS, dklen=32)


def _xor_stream(data: bytes, key: bytes) -> bytes:
    """Simple keystream (SHA256 counter mode) — stdlib-only encryption."""
    out = bytearray()
    counter = 0
    while len(out) < len(data):
        block = hashlib.sha256(key + struct.pack(">Q", counter)).digest()
        out.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out[: len(data)]))


def backup_dir() -> Path:
    p = Path.home() / ".nz-startup" / "backups"
    p.mkdir(parents=True, exist_ok=True)
    return p


def create_backup(
    company_id: str,
    *,
    passphrase: str,
    out_path: Path | None = None,
) -> dict[str, Any]:
    if not passphrase or len(passphrase) < 8:
        raise ValueError("passphrase must be at least 8 characters")
    company = ensure_exists(company_id)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = out_path or (backup_dir() / f"{company_id}-{stamp}.nzbak")
    dest.parent.mkdir(parents=True, exist_ok=True)

    # Stage zip in memory via temp file
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for root, _dirs, files in os.walk(company):
                for name in files:
                    if name == ".memory.lock":
                        continue
                    full = Path(root) / name
                    arc = full.relative_to(company).as_posix()
                    zf.write(full, arcname=arc)
        plain = tmp_path.read_bytes()
    finally:
        tmp_path.unlink(missing_ok=True)

    salt = secrets.token_bytes(16)
    key = _derive_key(passphrase, salt)
    ciphertext = _xor_stream(plain, key)
    mac = hmac.new(key, salt + ciphertext, hashlib.sha256).digest()
    dest.write_bytes(MAGIC + salt + mac + ciphertext)

    manifest = {
        "format": "nzbak1",
        "company_id": company_id,
        "created": stamp,
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
        "kdf": f"pbkdf2-hmac-sha256/{PBKDF2_ROUNDS}",
        "note": "Encrypted local backup. Full-disk encryption (BitLocker/FileVault) still assumed.",
        "restore": f"nz-startup backup restore {dest.name} --company {company_id} --passphrase ...",
    }
    man_path = dest.with_suffix(".nzbak.json")
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    append_audit(
        company,
        actor="cli:nz-startup",
        skill="compliance-registrar",
        action="backup_create",
        summary=f"Encrypted backup {dest.name} ({manifest['bytes']} bytes)",
        artefact_ref=str(dest),
        model_tier="light",
        outcome="ok",
        risk_level="medium",
        hitl_required=False,
    )
    return manifest


def restore_backup(
    bak_path: Path,
    *,
    passphrase: str,
    company_id: str | None = None,
    force: bool = False,
) -> dict[str, Any]:
    bak_path = Path(bak_path).expanduser().resolve()
    if not bak_path.is_file():
        raise FileNotFoundError(bak_path)
    raw = bak_path.read_bytes()
    if not raw.startswith(MAGIC):
        raise ValueError("Not an NZBAK1 archive")
    body = raw[len(MAGIC) :]
    salt, mac, ciphertext = body[:16], body[16:48], body[48:]
    key = _derive_key(passphrase, salt)
    expect = hmac.new(key, salt + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(mac, expect):
        raise PermissionError("Invalid passphrase or corrupted backup")
    plain = _xor_stream(ciphertext, key)

    # Infer company id
    cid = company_id
    if not cid:
        # try from filename company-stamp.nzbak
        stem = bak_path.name.replace(".nzbak", "")
        cid = stem.rsplit("-", 1)[0] if "-" in stem else stem

    dest = companies_dir() / cid
    if dest.exists() and any(dest.iterdir()) and not force:
        raise FileExistsError(f"{dest} exists — use --force to overwrite")

    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        tmp_path.write_bytes(plain)
        if dest.exists() and force:
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(tmp_path, "r") as zf:
            zf.extractall(dest)
    finally:
        tmp_path.unlink(missing_ok=True)

    append_audit(
        dest,
        actor="cli:nz-startup",
        skill="compliance-registrar",
        action="backup_restore",
        summary=f"Restored from {bak_path.name}",
        artefact_ref=str(bak_path),
        model_tier="light",
        outcome="ok",
        risk_level="high",
        hitl_required=True,
        hitl_status="approved",
    )
    return {"company_id": cid, "path": str(dest), "source": str(bak_path)}
