"""
Hardened agent guardrails for NZ Start-Up in a Box.

Layers:
1. Autonomy ceiling (inform/draft/prepare/monitor/remind only)
2. Path sandbox (company memory only)
3. Secret / PII pattern refusal
4. Output watermarking requirements
5. Risk classification for specialist routing
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from nz_startup.hitl import FORBIDDEN_TOOL_NAMES, WATERMARKS, check_action
from nz_startup.paths import company_dir, memory_root

AUTONOMY_SLOGAN = (
    "Agents inform, draft, prepare, monitor, and remind. "
    "Humans advise, sign, file, send, and pay."
)

# Patterns that must never be written to memory or logs
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("aws_key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("generic_api_key", re.compile(r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}")),
    ("bearer_jwt", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("password_assign", re.compile(r"(?i)password\s*[:=]\s*\S{6,}")),
    ("connection_string", re.compile(r"(?i)(postgres|mysql|mongodb)://[^\s]+:[^\s]+@")),
]

# Soft PII — warn / block write to git-tracked paths
PII_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ird_like", re.compile(r"\b\d{2,3}[-\s]?\d{3}[-\s]?\d{3}\b")),  # also GST; context-dependent
    ("nz_bank_account", re.compile(r"\b\d{2}[-\s]?\d{4}[-\s]?\d{7}[-\s]?\d{2,3}\b")),
    ("credit_card", re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
]

ALLOWED_AUTONOMY = frozenset(
    {"inform", "draft", "prepare", "monitor", "remind", "triage", "export_local", "read"}
)
FORBIDDEN_AUTONOMY = frozenset(
    {"advise", "send", "pay", "sign", "submit", "claim", "deploy_prod", "exfiltrate"}
)


class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GuardResult:
    allowed: bool
    risk: RiskTier
    reasons: list[str] = field(default_factory=list)
    requires_hitl: bool = False
    cultural_sensitivity: str = "low"
    watermarks_required: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "risk": self.risk.value,
            "reasons": self.reasons,
            "requires_hitl": self.requires_hitl,
            "cultural_sensitivity": self.cultural_sensitivity,
            "watermarks_required": self.watermarks_required,
            "autonomy_slogan": AUTONOMY_SLOGAN,
        }


def classify_risk(action: str, context: str = "", skill: str = "") -> GuardResult:
    """Classify risk and apply hard blocks."""
    reasons: list[str] = []
    score = 0
    text = f"{action} {context} {skill}".lower()

    hitl = check_action(action)
    if not hitl.allowed:
        return GuardResult(
            allowed=False,
            risk=RiskTier.CRITICAL,
            reasons=[hitl.reason],
            requires_hitl=True,
            watermarks_required=[WATERMARKS["agent"]],
        )

    for frag in FORBIDDEN_AUTONOMY:
        if frag in text.replace("-", " ").replace("_", " "):
            # only hard-block when clearly operational intent
            if any(
                p in text
                for p in (
                    "file ",
                    "send ",
                    "pay ",
                    "sign ",
                    "submit ",
                    "wire ",
                    "transfer money",
                )
            ):
                return GuardResult(
                    allowed=False,
                    risk=RiskTier.CRITICAL,
                    reasons=[f"Forbidden autonomy verb: {frag}"],
                    requires_hitl=True,
                )

    high_keywords = (
        "ird",
        "gst return",
        "tax",
        "legal advice",
        "financial advice",
        "nda",
        "employment",
        "privacy act",
        "personal data",
        "bank",
        "invoice",
        "funding",
        "investor",
        "safe note",
        "maori",
        "māori",
        "iwi",
        "whanau",
        "whānau",
        "whenua",
    )
    for kw in high_keywords:
        if kw in text:
            score += 2
            reasons.append(f"High-risk domain: {kw}")

    cultural = "low"
    cultural_hits = sum(
        1
        for kw in ("maori", "māori", "iwi", "whanau", "whānau", "whenua", "te tiriti", "tikanga")
        if kw in text
    )
    if cultural_hits >= 2:
        cultural = "high"
        score += 2
        reasons.append("Elevated cultural sensitivity")
    elif cultural_hits == 1:
        cultural = "medium"
        score += 1

    watermarks: list[str] = [WATERMARKS["agent"]]
    if any(k in text for k in ("legal", "nda", "contract", "agreement")):
        watermarks.append(WATERMARKS["legal"])
        score += 1
    if any(k in text for k in ("gst", "tax", "invoice", "xero", "bank")):
        watermarks.append(WATERMARKS["finance"])
        score += 1
    if any(k in text for k in ("outreach", "email", "cold")):
        watermarks.append(WATERMARKS["outreach"])
        score += 2
        reasons.append("Outreach must remain DRAFT_NOT_SENT")
    if any(k in text for k in ("compliance", "annual return", "privacy")):
        watermarks.append(WATERMARKS["compliance"])

    if score >= 6:
        risk = RiskTier.CRITICAL
        requires_hitl = True
    elif score >= 4:
        risk = RiskTier.HIGH
        requires_hitl = True
    elif score >= 2:
        risk = RiskTier.MEDIUM
        requires_hitl = True
    else:
        risk = RiskTier.LOW
        requires_hitl = False

    # High/critical always HITL for specialist outputs
    if skill in (
        "legal-document-assistant",
        "finance-clerk",
        "funding-analyst",
        "gtm-pipeline-rep",
        "grants-rdti-clerk",
    ):
        requires_hitl = True
        if risk == RiskTier.LOW:
            risk = RiskTier.MEDIUM
        reasons.append(f"Skill '{skill}' requires HITL by policy")

    return GuardResult(
        allowed=True,
        risk=risk,
        reasons=reasons or ["Within autonomy ceiling"],
        requires_hitl=requires_hitl,
        cultural_sensitivity=cultural,
        watermarks_required=list(dict.fromkeys(watermarks)),
    )


def scan_secrets(content: str) -> list[str]:
    hits: list[str] = []
    for name, pattern in SECRET_PATTERNS:
        if pattern.search(content or ""):
            hits.append(name)
    return hits


def scan_pii_soft(content: str) -> list[str]:
    hits: list[str] = []
    for name, pattern in PII_PATTERNS:
        if pattern.search(content or ""):
            hits.append(name)
    return hits


def assert_safe_write_content(content: str, *, allow_soft_pii: bool = True) -> None:
    secrets = scan_secrets(content)
    if secrets:
        raise PermissionError(
            f"Refusing write: secret-like patterns detected ({', '.join(secrets)}). "
            "Never store keys, tokens, or passwords in company memory."
        )
    if not allow_soft_pii:
        pii = scan_pii_soft(content)
        if pii:
            raise PermissionError(
                f"Refusing write: soft PII patterns ({', '.join(pii)}). "
                "Keep IRD/bank details out of git-backed memory."
            )


def resolve_sandboxed_path(company_id: str, relative: str) -> Path:
    """Ensure path stays under company memory root."""
    base = company_dir(company_id).resolve()
    # reject absolute escapes
    rel = relative.replace("\\", "/").lstrip("/")
    if ".." in Path(rel).parts:
        raise PermissionError("Path traversal rejected")
    path = (base / rel).resolve()
    try:
        path.relative_to(base)
    except ValueError as e:
        raise PermissionError("Path escapes company memory sandbox") from e
    # also ensure under memory root
    mem = memory_root().resolve()
    try:
        path.relative_to(mem)
    except ValueError as e:
        raise PermissionError("Path outside memory root") from e
    return path


def harden_mcp_tool_name(name: str) -> None:
    from nz_startup.hitl import assert_tool_name_allowed

    assert_tool_name_allowed(name)
    lowered = name.lower()
    for bad in ("send", "file_ird", "pay", "submit", "sign", "realme"):
        if bad in lowered and bad not in ("signed",):  # avoid false positive on "designed"
            if bad == "sign" and "design" in lowered:
                continue
            if any(x in lowered for x in ("send", "file_ird", "pay", "submit", "sign", "realme")):
                if name in FORBIDDEN_TOOL_NAMES or any(
                    name.startswith(p) for p in ("send_", "file_", "pay_", "submit_", "sign_")
                ):
                    raise PermissionError(f"Hardened MCP refuses tool name: {name}")


def skill_policy_block(skill_name: str) -> str:
    """Markdown block to append / inject into skill sessions."""
    return f"""
## HARDENED AUTONOMY (mandatory)

Skill: `{skill_name}`

{AUTONOMY_SLOGAN}

### Never
- File with Companies Office / IRD / myIR
- Send email/SMS (UEM Act 2007)
- Move money or create Xero payments
- Present drafts as legal or financial advice
- Store API keys, passwords, PEMs, or bank credentials in memory
- Invent NZBN, IRD numbers, hours, or partner consent

### Always
- Label drafts with watermarks (`DRAFT`, `NOT LEGAL ADVICE`, `DRAFT_NOT_SENT`, etc.)
- Prefer local-first data (Te Mana Raraunga)
- Escalate cultural / whenua / iwi framing for human review
- Log material actions to `audit.jsonl` when using runtime tools

### Risk
Use `nz-startup` guardrails: high/critical domain work requires HITL before human acts on output.
"""


def guardrails_status() -> dict[str, Any]:
    return {
        "version": "1.3.0",
        "licence": "proprietary",
        "autonomy_slogan": AUTONOMY_SLOGAN,
        "forbidden_tools": sorted(FORBIDDEN_TOOL_NAMES),
        "allowed_autonomy": sorted(ALLOWED_AUTONOMY),
        "forbidden_autonomy": sorted(FORBIDDEN_AUTONOMY),
        "watermarks": WATERMARKS,
        "secret_pattern_count": len(SECRET_PATTERNS),
        "sandbox": "company memory under NZ_STARTUP_MEMORY only",
        "compliance_gate": "nz-startup compliance check",
    }
