"""Coastal Alpine Tech pre-seed branding constants (single source of truth)."""

from __future__ import annotations

COMPANY_LEGAL = "Coastal Alpine Tech Limited"
COMPANY_SHORT = "Coastal Alpine Tech"
STAGE = "Pre-seed"
REGION = "Taranaki, Aotearoa New Zealand"
RD_START = "2025-08-08"
FOUNDING_DATE = "2026-08-08"
RD_START_DISPLAY = "8 August 2025"
FOUNDING_DISPLAY = "8 August 2026"
FOUNDER_CONTEXT = (
    "Wayne Roberts and Taranaki whānau — six generations in agriculture in Taranaki"
)
PRODUCT_NAME = "NZ Start-Up in a Box"
COPYRIGHT_YEARS = "2025–2026"
LICENCE_POSTURE = "dual-licence (proprietary Track A + commercial Track B)"
BUILD_TOOLS = (
    "Grok 4.5 Build",
    "Claude Pro Code",
    "Claude Computer Use",
    "Google Gemini 3.5 Flash",
)

# Global investor one-liner (portfolio consistency — report 9, 2026-07-15)
INVESTOR_ONE_LINER = (
    "Coastal Alpine Tech is building the sovereign hybrid edge-AI stack for Aotearoa’s "
    "primary industries and founders — local-first RPi 5 + Hailo nodes, multi-model fleets "
    "(Grok/Claude/Gemini), Te Mana Raraunga data sovereignty, and white-label EDA tools — "
    "actively seeking collaboration with Venture Taranaki, startups.com investors, and the "
    "Kotahitanga Investment Fund to scale intergenerational Māori and regional economic outcomes."
)
INVESTOR_ONE_LINER_SHORT = (
    "Sovereign hybrid edge AI for NZ farms & founders — local-first + multi-model, "
    "Te Mana Raraunga aligned — collaborating with Venture Taranaki, startups.com investors "
    "& Kotahitanga Investment Fund."
)
COLLABORATION_NOTE = (
    "Open to collaboration with Venture Taranaki, startups.com investors, "
    "and Kotahitanga Investment Fund (HITL + cultural advisory for any formal approach)."
)
HYBRID_DEFINITION = (
    "Hybrid edge + multi-model fleet: RPi 5 16GB + Hailo-10H (edge) · workstation companions · "
    "light/standard/frontier model tiers · local-first Te Mana Raraunga data · CAT Gold/Diamond/Platinum"
)

COPYRIGHT_LINE = (
    f"Copyright © {COPYRIGHT_YEARS} {COMPANY_LEGAL}. All rights reserved. "
    f"{STAGE}. R&D since {RD_START_DISPLAY}. Founded {FOUNDING_DISPLAY}."
)

HEADER_BANNER = f"""\
# {PRODUCT_NAME}
# {COMPANY_LEGAL} — {STAGE}
# {REGION}
# R&D commenced {RD_START_DISPLAY} · Founding date {FOUNDING_DISPLAY}
# Dual licence: proprietary default + commercial track (NZ Copyright Act 1994)
# {FOUNDER_CONTEXT}
# Built with: {", ".join(BUILD_TOOLS)}
# {COPYRIGHT_LINE}
"""


def about_dict() -> dict:
    return {
        "company": COMPANY_LEGAL,
        "stage": STAGE,
        "region": REGION,
        "rd_start": RD_START,
        "founding_date": FOUNDING_DATE,
        "founder_context": FOUNDER_CONTEXT,
        "product": PRODUCT_NAME,
        "licence": LICENCE_POSTURE,
        "build_tools": list(BUILD_TOOLS),
        "copyright": COPYRIGHT_LINE,
        "investor_one_liner": INVESTOR_ONE_LINER,
        "investor_one_liner_short": INVESTOR_ONE_LINER_SHORT,
        "collaboration": COLLABORATION_NOTE,
        "hybrid": HYBRID_DEFINITION,
    }
