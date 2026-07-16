#!/usr/bin/env bash
# EDA / Venture Taranaki style demo - Unix
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> NZ Start-Up in a Box - EDA demo"
python3 -m pip install -e ".[dev]" -q
python3 -m nz_startup demo run --company demo-eda --partner "Venture Taranaki" --programme "PowerUp demo"
echo ""
echo "Open: memory/companies/demo-eda/demo/demo-report-latest.md"
echo "Optional cohort pack:"
echo ' python3 -m nz_startup cohort init vt-powerup --partner "Venture Taranaki" --programme "PowerUp"'
echo " python3 -m nz_startup cohort pack vt-powerup"
