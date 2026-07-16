"""Read-only NZBN / Companies Office style lookup helpers."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# Public API base - requires subscription key for live calls.
# Docs: https://api.business.govt.nz/
DEFAULT_BASE = "https://api.business.govt.nz/gateway/nzbn/v5"


class NzbnError(RuntimeError):
 pass


def _api_key() -> str | None:
 return os.environ.get("BUSINESS_GOVT_API_KEY") or os.environ.get("NZBN_API_KEY")


def lookup_entities(query: str, *, limit: int = 5) -> dict[str, Any]:
 """
 Search entities by name or NZBN.

 Without an API key, returns an offline guidance payload so agents
 can still prepare formation packs without fabricating NZBNs.
 """
 q = (query or "").strip()
 if not q:
 raise ValueError("query is required")
 key = _api_key()
 if not key:
 return {
 "mode": "offline",
 "query": q,
 "entities": [],
 "message": (
 "No BUSINESS_GOVT_API_KEY set. Do not invent NZBNs. "
 "Founder should verify names on the Companies Office website "
 "or set a read-only API key from api.business.govt.nz."
 ),
 "human_actions": [
 "Search https://companies-register.companiesoffice.govt.nz/",
 "Reserve / register only via authenticated RealMe session",
 "Optional: obtain NZBN API access and set BUSINESS_GOVT_API_KEY",
 ],
 "hitl": "Founder verifies and files - agent prepares only",
 }

 # Live search - endpoint shape may vary by gateway version; keep defensive.
 base = os.environ.get("NZBN_API_BASE", DEFAULT_BASE).rstrip("/")
 url = f"{base}/entities?search-term={urllib.parse.quote(q)}&page-size={int(limit)}"
 req = urllib.request.Request(
 url,
 headers={
 "Accept": "application/json",
 "Ocp-Apim-Subscription-Key": key,
 "User-Agent": "nz-startup-in-a-box/0.2 (read-only)",
 },
 method="GET",
 )
 try:
 with urllib.request.urlopen(req, timeout=20) as resp:
 raw = resp.read().decode("utf-8")
 data = json.loads(raw) if raw else {}
 except urllib.error.HTTPError as e:
 body = e.read().decode("utf-8", errors="replace")[:500]
 raise NzbnError(f"NZBN API HTTP {e.code}: {body}") from e
 except urllib.error.URLError as e:
 raise NzbnError(f"NZBN API network error: {e}") from e

 return {
 "mode": "live",
 "query": q,
 "raw": data,
 "hitl": "Read-only lookup. Filing still requires human RealMe session.",
 "note": "Treat results as informational; re-check before incorporation.",
 }


def format_lookup_markdown(result: dict[str, Any]) -> str:
 lines = [
 "# NZBN / name lookup",
 "",
 f"- Mode: `{result.get('mode')}`",
 f"- Query: {result.get('query')}",
 f"- HITL: {result.get('hitl')}",
 "",
 ]
 if result.get("mode") == "offline":
 lines.append(result.get("message", ""))
 lines.append("")
 lines.append("## Human actions")
 for a in result.get("human_actions", []):
 lines.append(f"- {a}")
 else:
 lines.append("## API payload (truncated)")
 lines.append("```json")
 lines.append(json.dumps(result.get("raw", {}), indent=2)[:4000])
 lines.append("```")
 lines.append("")
 lines.append("DRAFT - NOT FOR SUBMISSION - founder files in own session.")
 return "\n".join(lines)
