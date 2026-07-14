#!/usr/bin/env bash
# NZ Start-Up in a Box — install into Aether skills + local package
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "==> Installing nz-startup-in-a-box (editable)"
python3 -m pip install -e ".[dev]"

AETHER_SKILLS="${AETHER_SKILLS_PATH:-$HOME/.aether/skills}"
echo "==> Installing fleet skills → $AETHER_SKILLS"
python3 -m nz_startup install-skills --target "$AETHER_SKILLS" --mode copy

echo "==> Validating skills"
python3 scripts/validate_skills.py
python3 -m pytest -q
python3 -m nz_startup doctor
python3 -m nz_startup smoke

echo ""
echo "Done (v1.0). Next:"
echo "  nz-startup onboard my-startup --legal-name 'My Labs Limited'"
echo "  nz-startup console --port 8765"
echo "  nz-startup demo run --partner 'Venture Taranaki'"
echo "  See RELEASE.md and docs/GETTING_STARTED.md"
