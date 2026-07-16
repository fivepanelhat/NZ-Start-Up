"""T7/T7* - Encrypted local backup of company memory (data-at-rest).

Preferred path: Fernet (cryptography package - default dependency since v1.6.1).
Fallback: stdlib PBKDF2 + SHA256 keystream (documented best-effort).
Always reports which encryption_path was used.

NOT a substitute for full-disk encryption (BitLocker / FileVault assumed).
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

MAGIC_FERNET = b"NZBAK2\n" # Fernet envelope
MAGIC_STREAM = b"NZBAK1\n" # stdlib keystream fallback
PBKDF2_ROUNDS = 200_000


def _has_cryptography() -> bool:
 try:
 import cryptography # noqa: F401

 return True
 except ImportError:
 return False


def encryption_backend() -> str:
 return "fernet-cryptography" if _has_cryptography() else "stdlib-pbkdf2-sha256-stream"


def _derive_key(passphrase: str, salt: bytes) -> bytes:
 return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, PBKDF2_ROUNDS, dklen=32)


def _xor_stream(data: bytes, key: bytes) -> bytes:
 out = bytearray()
 counter = 0
 while len(out) < len(data):
 block = hashlib.sha256(key + struct.pack(">Q", counter)).digest()
 out.extend(block)
 counter += 1
 return bytes(a ^ b for a, b in zip(data, out[: len(data)]))


def _fernet_encrypt(plain: bytes, passphrase: str) -> tuple[bytes, str]:
 from cryptography.hazmat.primitives import hashes
 from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
 from cryptography.fernet import Fernet
 import base64

 salt = secrets.token_bytes(16)
 kdf = PBKDF2HMAC(
 algorithm=hashes.SHA256(),
 length=32,
 salt=salt,
 iterations=PBKDF2_ROUNDS,
 )
 key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))
 token = Fernet(key).encrypt(plain)
 return MAGIC_FERNET + salt + token, "fernet-cryptography"


def _fernet_decrypt(body: bytes, passphrase: str) -> bytes:
 from cryptography.hazmat.primitives import hashes
 from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
 from cryptography.fernet import Fernet, InvalidToken
 import base64

 salt, token = body[:16], body[16:]
 kdf = PBKDF2HMAC(
 algorithm=hashes.SHA256(),
 length=32,
 salt=salt,
 iterations=PBKDF2_ROUNDS,
 )
 key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))
 try:
 return Fernet(key).decrypt(token)
 except InvalidToken as e:
 raise PermissionError("Invalid passphrase or corrupted backup") from e


def _stream_encrypt(plain: bytes, passphrase: str) -> tuple[bytes, str]:
 salt = secrets.token_bytes(16)
 key = _derive_key(passphrase, salt)
 ciphertext = _xor_stream(plain, key)
 mac = hmac.new(key, salt + ciphertext, hashlib.sha256).digest()
 return MAGIC_STREAM + salt + mac + ciphertext, "stdlib-pbkdf2-sha256-stream"


def _stream_decrypt(body: bytes, passphrase: str) -> bytes:
 salt, mac, ciphertext = body[:16], body[16:48], body[48:]
 key = _derive_key(passphrase, salt)
 expect = hmac.new(key, salt + ciphertext, hashlib.sha256).digest()
 if not hmac.compare_digest(mac, expect):
 raise PermissionError("Invalid passphrase or corrupted backup")
 return _xor_stream(ciphertext, key)


def backup_dir() -> Path:
 p = Path.home() / ".nz-startup" / "backups"
 p.mkdir(parents=True, exist_ok=True)
 return p


def _zip_company(company: Path) -> bytes:
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
 return tmp_path.read_bytes()
 finally:
 tmp_path.unlink(missing_ok=True)


def create_backup(
 company_id: str,
 *,
 passphrase: str,
 out_path: Path | None = None,
 prefer_fernet: bool = True,
) -> dict[str, Any]:
 if not passphrase or len(passphrase) < 8:
 raise ValueError("passphrase must be at least 8 characters")
 company = ensure_exists(company_id)
 stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
 dest = out_path or (backup_dir() / f"{company_id}-{stamp}.nzbak")
 dest.parent.mkdir(parents=True, exist_ok=True)

 plain = _zip_company(company)
 if prefer_fernet and _has_cryptography():
 blob, path_used = _fernet_encrypt(plain, passphrase)
 else:
 blob, path_used = _stream_encrypt(plain, passphrase)
 if prefer_fernet and not _has_cryptography():
 path_used = "stdlib-pbkdf2-sha256-stream (install cryptography for Fernet)"

 dest.write_bytes(blob)
 manifest = {
 "format": "nzbak2" if blob.startswith(MAGIC_FERNET) else "nzbak1",
 "company_id": company_id,
 "created": stamp,
 "path": str(dest),
 "bytes": dest.stat().st_size,
 "sha256": hashlib.sha256(blob).hexdigest(),
 "encryption_path": path_used,
 "kdf": f"pbkdf2-hmac-sha256/{PBKDF2_ROUNDS}",
 "cryptography_available": _has_cryptography(),
 "note": "Encrypted local backup. Full-disk encryption (BitLocker/FileVault) still assumed.",
 "restore": f"nz-startup backup restore --archive {dest.name} --company {company_id} --passphrase ...",
 }
 man_path = dest.with_suffix(".nzbak.json")
 man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

 append_audit(
 company,
 actor="cli:nz-startup",
 skill="compliance-registrar",
 action="backup_create",
 summary=f"Encrypted backup {dest.name} via {path_used} ({manifest['bytes']} bytes)",
 artefact_ref=str(dest),
 model_tier="light",
 outcome="ok",
 risk_level="medium",
 hitl_required=False,
 extra={"encryption_path": path_used},
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
 if raw.startswith(MAGIC_FERNET):
 if not _has_cryptography():
 raise RuntimeError(
 "This backup uses Fernet encryption - install cryptography: pip install cryptography"
 )
 plain = _fernet_decrypt(raw[len(MAGIC_FERNET) :], passphrase)
 path_used = "fernet-cryptography"
 elif raw.startswith(MAGIC_STREAM):
 plain = _stream_decrypt(raw[len(MAGIC_STREAM) :], passphrase)
 path_used = "stdlib-pbkdf2-sha256-stream"
 else:
 raise ValueError("Not an NZBAK1/NZBAK2 archive")

 cid = company_id
 if not cid:
 stem = bak_path.name.replace(".nzbak", "")
 cid = stem.rsplit("-", 1)[0] if "-" in stem else stem

 dest = companies_dir() / cid
 if dest.exists() and any(dest.iterdir()) and not force:
 raise FileExistsError(f"{dest} exists - use --force to overwrite")

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
 summary=f"Restored from {bak_path.name} via {path_used}",
 artefact_ref=str(bak_path),
 model_tier="light",
 outcome="ok",
 risk_level="high",
 hitl_required=True,
 hitl_status="approved",
 extra={"encryption_path": path_used},
 )
 return {
 "company_id": cid,
 "path": str(dest),
 "source": str(bak_path),
 "encryption_path": path_used,
 }
