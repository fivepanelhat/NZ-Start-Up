# Getting Started

## 1. Install

**Windows**

```powershell
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

**macOS / Linux**

```bash
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
chmod +x install.sh && ./install.sh
```

Manual:

```bash
python -m pip install -e ".[dev]"
nz-startup install-skills
nz-startup validate
```

## 2. Wire skills into your agent host

### Aether

`install.ps1` / `nz-startup install-skills` copies the fleet into `~/.aether/skills` (or `$AETHER_SKILLS_PATH`).

### Claude Code / similar

Point the skills root at `./skills`, or use the installed Aether path.

### MCP

```bash
pip install -e ".[mcp]"
# Register mcp.json with your host, or run:
nz-startup mcp
```

See `docs/MCP.md`.

## 3. Initialise company memory

```bash
# Recommended first hour
nz-startup onboard my-startup \
  --legal-name "Example Labs Limited" \
  --wedge "Your wedge" \
  --icp "Your ICP"

# Or bare init:
nz-startup init my-startup
```

Edit `memory/companies/my-startup/profile.md` with real (non-secret) facts.

## 4. Daily / weekly commands

```bash
# Contemporaneous RDTI log (do not invent hours)
nz-startup rdti add my-startup \
  --hours 2 \
  --activity "Edge offline inference experiment" \
  --uncertainty "Latency under offline constraint" \
  --evidence "commit:abc123"

# Pipeline (local CRM — never sends)
nz-startup pipeline add my-startup --account "Venture Taranaki" --stage discovery --next-step "intro call"
nz-startup pipeline update my-startup P001 --stage qualified --next-step "paid pilot offer"
nz-startup pipeline summary my-startup

# Calendar reminders
nz-startup calendar add my-startup --item "Annual return prep" --due 2027-08-01 --category compliance
nz-startup calendar remind my-startup --days 14

# Grants tracker
nz-startup grants rank my-startup
nz-startup grants update my-startup G001 --status drafting --next-action "complete budget skeleton"

# Outreach draft — never sends
nz-startup draft-outreach my-startup \
  --subject "Discovery chat" \
  --body "Kia ora ..."

# Name check guidance (live if BUSINESS_GOVT_API_KEY set)
nz-startup nzbn "My Proposed Limited"

# Xero read-only (offline demo without tokens)
nz-startup xero status
nz-startup xero snapshot my-startup --offline

# Bank feed + GST working papers (not a filing)
nz-startup bank import my-startup --file templates/bank-feed-sample.csv
nz-startup bank triage my-startup
nz-startup gst prepare my-startup --start 2026-07-01 --end 2026-07-31

# Invoice triage + accountant handoff zip (you deliver the zip)
nz-startup invoice triage my-startup --path templates/sample-tax-invoice.txt
nz-startup handoff pack my-startup

# White-label cohort + EDA demo
nz-startup cohort init vt-powerup --partner "Venture Taranaki" --programme "PowerUp"
nz-startup cohort add-seat vt-powerup --founder demo --company demo-seat
nz-startup cohort pack vt-powerup
nz-startup demo run --company demo-eda --partner "Venture Taranaki"
nz-startup status demo-eda
nz-startup board pack demo-eda
nz-startup smoke

# Deadline exports (import ICS yourself — agent does not email)
nz-startup export reminders my-startup --days 14 --ics-days 90

# Board pack (pipeline + calendar + grants + export refresh)
nz-startup weekly my-startup
```

## 5. First session prompts

**Bootstrap**

```text
Load nz-startup-fleet and cat-architectural-standards.
Classify this session. Initialise my company memory and produce a 30-day founder checklist for NZ incorporation.
```

**Weekly board**

```text
Load board-chief-of-staff.
Run weekly operating review using memory/companies/my-startup.
```

**RDTI habit**

```text
Load grants-rdti-clerk.
Append R&D activity log entries from my recent git commits. Do not invent hours.
```

## 6. Rules of engagement

- Every government filing pack ends with a **human action checklist**  
- Every outreach draft stays in Drafts until you send it  
- Every legal document is watermarked not advice  

## 7. Dogfooding path (Coastal Alpine Tech)

1. Run your own startup on this fleet as internal skills  
2. Show Venture Taranaki / EDA a working weekly board report  
3. If cohort pilot paid, wrap as white-label “Weaver Founder” vertical  
