# Sync NZ-Start-Up skills/ into Aether skills/nz-startup/
# Usage: powershell -ExecutionPolicy Bypass -File portfolio/sync_skills_to_aether.ps1 [-AetherPath path]
param(
 [string]$AetherPath = "C:\Users\Admin\source\portfolio-work\Aether"
)
$ErrorActionPreference = "Stop"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not (Test-Path "$PSScriptRoot\..\skills")) {
 $Root = Resolve-Path "$PSScriptRoot\.."
} else {
 $Root = Resolve-Path "$PSScriptRoot\.."
}
$Src = Join-Path $Root "skills"
if (-not (Test-Path $AetherPath)) {
 Write-Host "Cloning Aether..."
 gh repo clone fivepanelhat/Aether $AetherPath
}
$Dest = Join-Path $AetherPath "skills\nz-startup"
if (Test-Path $Dest) { Remove-Item -Recurse -Force $Dest }
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Copy-Item -Recurse -Force "$Src\*" $Dest\
Write-Host "Synced $(@(Get-ChildItem $Dest -Directory).Count) skills -> $Dest"
Write-Host "Commit in Aether when ready."
