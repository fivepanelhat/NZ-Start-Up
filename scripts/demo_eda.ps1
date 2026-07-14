# EDA / Venture Taranaki style demo — Windows
# Usage: powershell -ExecutionPolicy Bypass -File .\scripts\demo_eda.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "==> NZ Start-Up in a Box — EDA demo"
python -m pip install -e ".[dev]" -q
python -m nz_startup demo run --company demo-eda --partner "Venture Taranaki" --programme "PowerUp demo"
Write-Host ""
Write-Host "Open: memory/companies/demo-eda/demo/demo-report-latest.md"
Write-Host "Optional cohort pack:"
Write-Host '  python -m nz_startup cohort init vt-powerup --partner "Venture Taranaki" --programme "PowerUp"'
Write-Host "  python -m nz_startup cohort pack vt-powerup"
