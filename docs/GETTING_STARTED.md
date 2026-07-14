# Getting Started

## 1. Install

```bash
git clone https://github.com/fivepanelhat/NZ-Start-Up.git
cd NZ-Start-Up
python -m pip install -e ".[dev]"
python scripts/validate_skills.py
```

## 2. Wire skills into your agent host

### Aether

Copy or symlink `skills/*` into your Aether skills path, or set your environment to load this directory.

### Claude Code / similar

Point the skills root at `./skills`.

## 3. Initialise company memory

Copy the example:

```bash
cp -r memory/example-company memory/companies/my-startup
```

Edit `profile.md` and `decisions.md` with real (non-secret) facts.

## 4. First session prompts

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

## 5. Rules of engagement

- Every government filing pack ends with a **human action checklist**  
- Every outreach draft stays in Drafts until you send it  
- Every legal document is watermarked not advice  

## 6. Dogfooding path (Coastal Alpine Tech)

1. Run your own startup on this fleet as internal skills  
2. Show Venture Taranaki / EDA a working weekly board report  
3. If cohort pilot paid, wrap as white-label “Weaver Founder” vertical  
