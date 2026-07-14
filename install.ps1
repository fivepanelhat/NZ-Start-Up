# NZ Start-Up in a Box — Windows install into Aether skills + local package
# Usage: powershell -ExecutionPolicy Bypass -File .\install.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "==> Installing nz-startup-in-a-box (editable)"
python -m pip install -e ".[dev]"

$AetherSkills = Join-Path $env:USERPROFILE ".aether\skills"
if ($env:AETHER_SKILLS_PATH) { $AetherSkills = $env:AETHER_SKILLS_PATH }

Write-Host "==> Installing fleet skills → $AetherSkills"
python -m nz_startup install-skills --target $AetherSkills --mode copy

Write-Host "==> Validating skills"
python scripts\validate_skills.py
python -m pytest -q

Write-Host ""
Write-Host "Done. Next:"
Write-Host "  nz-startup init my-startup"
Write-Host "  nz-startup weekly my-startup"
Write-Host "  nz-startup mcp          # MCP stdio (pip install '.[mcp]' first)"
Write-Host "  See docs/GETTING_STARTED.md"
