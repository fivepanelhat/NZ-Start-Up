# NZ Start-Up in a Box - Windows install into Aether skills + local package
# Usage: powershell -ExecutionPolicy Bypass -File .\install.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "==> Installing nz-startup-in-a-box (editable)"
python -m pip install -e ".[dev]"

$AetherSkills = Join-Path $env:USERPROFILE ".aether\skills"
if ($env:AETHER_SKILLS_PATH) { $AetherSkills = $env:AETHER_SKILLS_PATH }

Write-Host "==> Installing fleet skills -> $AetherSkills"
python -m nz_startup install-skills --target $AetherSkills --mode copy

Write-Host "==> Validating skills"
python scripts\validate_skills.py
python -m pytest -q
python -m nz_startup doctor
python -m nz_startup smoke

Write-Host ""
Write-Host "Done (v1.0). Next:"
Write-Host " nz-startup onboard my-startup --legal-name `"My Labs Limited`""
Write-Host " nz-startup console --port 8765 --open"
Write-Host " nz-startup desktop"
Write-Host " nz-startup demo run --partner `"Venture Taranaki`""
Write-Host " See RELEASE.md and docs/GETTING_STARTED.md"
