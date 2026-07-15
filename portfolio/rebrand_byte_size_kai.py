#!/usr/bin/env python3
"""Foreground Byte Size Kai; background Blue-Moon as technical repo name."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

BM = Path(r"C:\Users\Admin\source\portfolio-work\Blue-Moon-Portal")
FP = Path(r"C:\Users\Admin\source\portfolio-work\fivepanelhat")
NZ = Path(r"C:\Users\Admin\source\NZ-Start-Up")


def write_utf8(path: Path, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.endswith("\n"):
        text += "\n"
    path.write_bytes(text.encode("utf-8"))


def fix_blue_moon_readme() -> None:
    p = BM / "README.md"
    t = p.read_text(encoding="utf-8", errors="replace")

    t = t.replace("# Blue Moon Portal: Byte Size Kai", "# Byte Size Kai")
    t = re.sub(
        r"\*\*Welcome to the Blue Moon Portal\*\*[^\n]*",
        (
            "**Byte Size Kai** is Coastal Alpine Tech's agritech product for sovereign, "
            "on-farm microgreen and crop intelligence. The engineering stack and GitHub "
            "repository path remain **Blue-Moon-Portal** (technical / package name) - use "
            "that for clones, CI, and Core SDK imports."
        ),
        t,
        count=1,
    )

    callout = """
## Product name vs stack name

| Name | Use |
|------|-----|
| **Byte Size Kai** | Product brand - growers, Mana Kai partners, and the [org front page](https://github.com/fivepanelhat/fivepanelhat) lead with this |
| **Blue-Moon-Portal** | Repository / edge portal package name (background technical identity) |

This repository implements **Byte Size Kai** on the Kiwi Edge stack (RPi 5 16GB + Hailo-10H, Core SDK, local Ollama).

"""
    if "Product name vs stack name" not in t:
        t = t.replace(
            "<!-- END CAT_CONGRUENCE_SNIPPET -->",
            "<!-- END CAT_CONGRUENCE_SNIPPET -->\n" + callout,
        )

    t = t.replace("![Blue Moon Portal Banner]", "![Byte Size Kai Banner]")
    t = t.replace("n-portal\npython bootstrap.py\n```\n", "")
    t = re.sub(r"ð[^\s]{1,10}\s*", "", t)
    t = t.replace("\ufffd", "")
    t = t.replace("blue-moon-portal.git", "Blue-Moon-Portal.git")
    t = t.replace("cd blue-moon-portal", "cd Blue-Moon-Portal")

    if "HITL for actuators" not in t and "Autonomy (edge agents)" not in t:
        t = t.replace(
            "## The Problems We Are Solving",
            """## Autonomy (edge agents)

Agents **inform, draft, prepare, monitor, and remind**. Physical actuation and commercial decisions stay human-in-the-loop unless an explicit local allow-list is configured on-site.

## The Problems We Are Solving""",
        )

    # Role line in CAT_CONGRUENCE if present
    write_utf8(p, t)

    cong = BM / "CAT_CONGRUENCE.md"
    if cong.is_file():
        c = cong.read_text(encoding="utf-8", errors="replace")
        c = c.replace(
            "Crop / microgreens domain portal",
            "Byte Size Kai product (Blue-Moon stack - agritech beachhead)",
        )
        if "Byte Size Kai" not in c.split("This repository")[-1] if "This repository" in c else True:
            if "## This repository" in c:
                c = re.sub(
                    r"(\| \*\*Role in stack\*\* \| )([^\n|]+)",
                    r"\1Byte Size Kai product (repo: Blue-Moon-Portal)",
                    c,
                    count=1,
                )
        write_utf8(cong, c)
    print("Blue-Moon-Portal product branding updated")


def fix_front_page() -> None:
    p = FP / "README.md"
    t = p.read_text(encoding="utf-8", errors="replace")

    t = t.replace(
        "| [Blue-Moon-Portal](https://github.com/fivepanelhat/Blue-Moon-Portal) | Multi-modal edge AI for microgreen cultivation | Edge Linux | Biosecurity Act 1993, HSNO Act 1996, Food Act 2014 | RPi 5 16GB + Hailo-10H |",
        "| [**Byte Size Kai**](https://github.com/fivepanelhat/Blue-Moon-Portal) (`Blue-Moon-Portal`) | **Lead agritech product** - multi-modal edge AI for microgreens / Mana Kai | Edge Linux | Biosecurity Act 1993, HSNO Act 1996, Food Act 2014 | RPi 5 16GB + Hailo-10H |",
    )
    t = re.sub(r'Blue\["Blue-Moon"\]', 'Blue["Byte Size Kai"]', t)
    t = re.sub(r"Blue\['Blue-Moon'\]", 'Blue["Byte Size Kai"]', t)

    featured = """
### Featured edge product: Byte Size Kai

**Byte Size Kai** is the forefront agritech offering on this stack - sovereign multi-modal crop intelligence for microgreens and Mana Kai-class growers (Horowhenua field context / Taranaki engineering).

| | |
|--|--|
| **Product brand** | Byte Size Kai |
| **Repository (technical / CI path)** | [Blue-Moon-Portal](https://github.com/fivepanelhat/Blue-Moon-Portal) - keep clone URLs as-is |
| **Stack role** | Domain portal on Coastal-Alpine-Core + Hailo vision + local Ollama |
| **Sister portals (background)** | SoilGuard, AquaGuard, Sting-Operation |

"""
    if "Featured edge product: Byte Size Kai" not in t:
        t = t.replace(
            "### Foundation roles (CAT design targets)",
            featured + "### Foundation roles (CAT design targets)",
        )

    # Portals layer note
    t = t.replace(
        "| **Portals** | Domain agents | Agritech, biosecurity, water, soil |",
        "| **Portals** | Domain agents | **Byte Size Kai** (agritech lead), biosecurity, water, soil |",
    )

    write_utf8(p, t)

    cong = FP / "CAT_CONGRUENCE.md"
    if cong.is_file():
        c = cong.read_text(encoding="utf-8", errors="replace")
        c = c.replace(
            "Blue-Moon-Portal, SoilGuard-Portal, AquaGuard-Portal, Sting-Operation-AI",
            "**Byte Size Kai** (Blue-Moon-Portal), SoilGuard-Portal, AquaGuard-Portal, Sting-Operation-AI",
        )
        write_utf8(cong, c)
    print("fivepanelhat front page updated")


def fix_nz_startup_docs() -> None:
    replacements = [
        (
            "Blue-Moon-Portal, SoilGuard-Portal, AquaGuard-Portal, Sting-Operation-AI",
            "**Byte Size Kai** (Blue-Moon-Portal), SoilGuard-Portal, AquaGuard-Portal, Sting-Operation-AI",
        ),
        (
            "Blue-Moon (crop/microgreens)",
            "Byte Size Kai / Blue-Moon stack (crop/microgreens)",
        ),
        (
            "| **Blue-Moon-Portal** | 4 | 3 | 4 | 5 | 4 | **20** | Agritech beachhead | Growers / Mana Kai class |",
            "| **Byte Size Kai** (`Blue-Moon-Portal`) | 4 | 3 | 4 | 5 | 4 | **20** | **Agritech lead product** | Growers / Mana Kai class |",
        ),
        (
            "Agritech founder on NZ-Start-Up → Blue-Moon/SoilGuard pilot",
            "Agritech founder on NZ-Start-Up → Byte Size Kai / SoilGuard pilot",
        ),
        (
            "Blue-Moon or SoilGuard + Core + Firmware",
            "Byte Size Kai (Blue-Moon) or SoilGuard + Core + Firmware",
        ),
        (
            'founder OS + Blue-Moon/SoilGuard/Sting edge nodes',
            'founder OS + Byte Size Kai / SoilGuard / Sting edge nodes',
        ),
        (
            "Bundle with Blue-Moon/SoilGuard",
            "Bundle with Byte Size Kai / SoilGuard",
        ),
        (
            "Edge agritech stack (Blue-Moon, SoilGuard, Sting…)",
            "Edge agritech stack (Byte Size Kai, SoilGuard, Sting…)",
        ),
        (
            '"Blue-Moon-Portal": "Crop / microgreens domain portal"',
            '"Blue-Moon-Portal": "Byte Size Kai product (Blue-Moon stack)"',
        ),
    ]

    paths = [
        NZ / "CAT_CONGRUENCE.md",
        NZ / "portfolio" / "congruence-pack" / "CAT_CONGRUENCE.md",
        NZ / "docs" / "PORTFOLIO_MARKET_FIT.md",
        NZ / "docs" / "MARKET_FIT_MATRIX.md",
        NZ / "docs" / "MARKET.md",
        NZ / "docs" / "SEED_INVESTOR_PACK.md",
        NZ / "portfolio" / "fix_encoding.py",
        NZ / "nz_startup" / "market_fit.py",
    ]
    for path in paths:
        if not path.is_file():
            continue
        t = path.read_text(encoding="utf-8", errors="replace")
        orig = t
        for a, b in replacements:
            t = t.replace(a, b)
        # market_fit portfolio role
        t = t.replace(
            '{"repo": "Blue-Moon-Portal", "total": 20, "role": "Agritech beachhead", "buyer": "Growers"}',
            '{"repo": "Blue-Moon-Portal", "total": 20, "role": "Byte Size Kai (agritech lead)", "buyer": "Growers / Mana Kai"}',
        )
        if t != orig:
            write_utf8(path, t)
            print("updated", path.relative_to(NZ))


def git_push(repo: Path, message: str) -> None:
    def run(args: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(args, cwd=str(repo), capture_output=True, text=True)

    run(["git", "add", "-A"])
    st = run(["git", "status", "--porcelain"])
    if not st.stdout.strip():
        print(repo.name, "clean")
        return
    run(["git", "commit", "-m", message])
    p = run(["git", "push", "origin", "HEAD"])
    print(repo.name, "push", p.returncode, (p.stderr or p.stdout)[-200:])


def main() -> None:
    fix_blue_moon_readme()
    fix_front_page()
    fix_nz_startup_docs()

    # GitHub description
    subprocess.run(
        [
            "gh",
            "repo",
            "edit",
            "fivepanelhat/Blue-Moon-Portal",
            "--description",
            "Byte Size Kai - sovereign multi-modal edge agritech for microgreens / Mana Kai (technical stack: Blue-Moon-Portal on Core + RPi 5 16GB + Hailo-10H).",
        ],
        check=False,
    )

    git_push(
        BM,
        "docs: foreground Byte Size Kai product; Blue-Moon as technical stack name",
    )
    git_push(
        FP,
        "docs: feature Byte Size Kai as lead agritech product on main",
    )
    git_push(
        NZ,
        "docs: portfolio congruence - Byte Size Kai forefront, Blue-Moon background",
    )


if __name__ == "__main__":
    main()
