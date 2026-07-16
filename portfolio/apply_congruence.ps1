# Apply CAT congruence pack to all fivepanelhat repos.
# Requires: gh authenticated, git, network.
$ErrorActionPreference = "Stop"
$Org = "fivepanelhat"
$Work = "C:\Users\Admin\source\portfolio-work"
$Pack = "C:\Users\Admin\source\NZ-Start-Up\portfolio\congruence-pack"
$Repos = @(
  "fivepanelhat",
  "Aether",
  "Weaver",
  "Coastal-Alpine-Core",
  "coastal-alpine-stack",
  "Sovereign-Edge-Firmware",
  "Byte-Size-Kai",
  "SoilGuard-Portal",
  "AquaGuard-Portal",
  "Sting-Operation-AI",
  "whanau-preterm-support-hub",
  "Front_Line_Whanau",
  "CAT-mail",
  "NZ-Start-Up"
)

New-Item -ItemType Directory -Force -Path $Work | Out-Null
$results = @()

function Copy-PackInto([string]$dest) {
  Copy-Item -Force "$Pack\CAT_CONGRUENCE.md" "$dest\CAT_CONGRUENCE.md"
  New-Item -ItemType Directory -Force -Path "$dest\.github\agent-fleet" | Out-Null
  Copy-Item -Recurse -Force "$Pack\.github\agent-fleet\*" "$dest\.github\agent-fleet\"
  # Root AGENTS.md mirrors fleet policy for tools that only look at root
  Copy-Item -Force "$Pack\.github\agent-fleet\AGENTS.md" "$dest\AGENTS.md"
}

function Ensure-ReadmeSnippet([string]$dest) {
  $readme = Join-Path $dest "README.md"
  if (-not (Test-Path $readme)) { return }
  $text = Get-Content $readme -Raw -ErrorAction SilentlyContinue
  if ($null -eq $text) { return }
  $snippetPath = "$Pack\README_SNIPPET.md"
  $snippet = Get-Content $snippetPath -Raw
  if ($text -match "BEGIN CAT_CONGRUENCE_SNIPPET") {
    $text = [regex]::Replace($text, "(?s)<!-- BEGIN CAT_CONGRUENCE_SNIPPET -->.*?<!-- END CAT_CONGRUENCE_SNIPPET -->", $snippet.Trim())
  } else {
    # Insert after first heading block
    if ($text -match "(?s)^(#[^\n]+\n)") {
      $text = $text -replace "(?s)^(#[^\n]+\n)", "`$1`n$snippet`n"
    } else {
      $text = $snippet + "`n`n" + $text
    }
  }
  Set-Content -Path $readme -Value $text -Encoding utf8 -NoNewline
}

foreach ($repo in $Repos) {
  $dir = Join-Path $Work $repo
  Write-Host "==== $repo ====" -ForegroundColor Cyan
  try {
    if ($repo -eq "NZ-Start-Up") {
      $dir = "C:\Users\Admin\source\NZ-Start-Up"
    } elseif ($repo -eq "Front_Line_Whanau" -and (Test-Path "C:\Users\Admin\source\front_line_whanau")) {
      $dir = "C:\Users\Admin\source\front_line_whanau"
    } else {
      if (Test-Path $dir) {
        Push-Location $dir
        git fetch origin 2>$null
        git checkout main 2>$null
        if ($LASTEXITCODE -ne 0) { git checkout master 2>$null }
        git pull --ff-only origin HEAD 2>$null
        Pop-Location
      } else {
        gh repo clone "$Org/$repo" $dir -- --depth 1
      }
    }
    if (-not (Test-Path $dir)) { throw "clone missing $dir" }

    Copy-PackInto $dir
    Ensure-ReadmeSnippet $dir

    # Repo-specific congruence role line
    $role = switch ($repo) {
      "fivepanelhat" { "Org landing / architecture map" }
      "NZ-Start-Up" { "Founder OS + EDA white-label (seed wedge)" }
      "Aether" { "Agent skills, HITL, orchestration companion" }
      "Weaver" { "Multi-tenant edge orchestration + local RAG" }
      "Coastal-Alpine-Core" { "Shared edge SDK (SecurityGuard, MQTT, flywheel)" }
      "coastal-alpine-stack" { "Full-stack edge monorepo / deploy" }
      "Sovereign-Edge-Firmware" { "ESP32 field layer / mTLS MQTT" }
      "Byte-Size-Kai" { "Crop / microgreens domain portal" }
      "SoilGuard-Portal" { "Soil & pasture domain portal" }
      "AquaGuard-Portal" { "Water & aquaculture domain portal" }
      "Sting-Operation-AI" { "Biosecurity vision sentinel" }
      "whanau-preterm-support-hub" { "Whānau preterm support (cultural HITL primary)" }
      "Front_Line_Whanau" { "Frontline whānau services platform" }
      "CAT-mail" { "Privacy-first email assist" }
      default { "Kiwi Edge stack component" }
    }
    $cong = Get-Content "$dir\CAT_CONGRUENCE.md" -Raw
    if ($cong -notmatch "## This repository") {
      $extra = @"

## This repository

| Field | Value |
|-------|-------|
| **Repo** | ``$repo`` |
| **Role in stack** | $role |
| **Agent fleet** | ``.github/agent-fleet/`` |
| **Canonical skills runtime** | [NZ-Start-Up](https://github.com/fivepanelhat/NZ-Start-Up) |

"@
      Add-Content -Path "$dir\CAT_CONGRUENCE.md" -Value $extra -Encoding utf8
    }

    Push-Location $dir
    git add CAT_CONGRUENCE.md AGENTS.md .github/agent-fleet README.md 2>$null
    $status = git status --porcelain
    if (-not $status) {
      Write-Host "no changes"
      $results += [pscustomobject]@{ repo = $repo; status = "clean" }
      Pop-Location
      continue
    }
    git commit -m "chore: CAT portfolio congruence + anti-hallucination agent fleet" -m "Add CAT_CONGRUENCE.md, AGENTS.md, .github/agent-fleet (hardening, anti-hallucination, Gold/Diamond/Platinum). Align with fivepanelhat front page and NZ-Start-Up HITL/autonomy ceilings. Refusal calibration and FACT/INFERENCE/UNKNOWN labels to reduce hallucination."
    git push origin HEAD
    $results += [pscustomobject]@{ repo = $repo; status = "pushed" }
    Pop-Location
  } catch {
    Write-Host "ERROR $repo : $_" -ForegroundColor Red
    $results += [pscustomobject]@{ repo = $repo; status = "error: $_" }
    if (Get-Location | Where-Object { $_.Path -like "*portfolio*" -or $_.Path -like "*NZ*" -or $_.Path -like "*front*" }) {
      Pop-Location -ErrorAction SilentlyContinue
    }
  }
}

$results | Format-Table -AutoSize
$results | ConvertTo-Json | Set-Content "$Work\congruence-results.json" -Encoding utf8
Write-Host "Done. Results: $Work\congruence-results.json"
