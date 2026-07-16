# Cold-start film runbook (skills pack)

**Purpose:** Record a short (3-6 min) proof that a clean Windows machine can install NZ Start-Up and produce a board pack offline-capable path.

**Status:** Human films. Agent prepares this checklist only.  
**Pack:** `dist/nz-startup-skills-pack-latest.zip` (also on OneDrive SuperGrok pack)

---

## Props

1. Clean Windows 10/11 user (or VM) without prior CAT install.
2. Python 3.10+ from python.org.
3. Skills pack zip + `.sha256` file from `dist/` or OneDrive.
4. Optional: screen recorder (Xbox Game Bar / OBS).

---

## Script (spoken + on screen)

1. **Show integrity:** open sha256 file; note pack version.
2. **Unzip** pack to `C:\cat\nz-startup` (or Desktop).
3. **Install:**

```powershell
cd C:\cat\nz-startup   # or extracted path
python -m pip install -e ".[dev]"
python -m nz_startup doctor
python -m nz_startup smoke
```

4. **Demo for EDA:**

```powershell
python -m nz_startup demo run --company demo-vt --partner "Venture Taranaki" --programme "PowerUp demo"
python -m nz_startup status demo-vt
python -m nz_startup board pack demo-vt
```

5. **Show trust ceilings:**

```powershell
python -m nz_startup compliance check
python -m nz_startup harden status
```

6. **Close line (say out loud):**  
   "Agents draft and prepare. Humans file, send, pay, and sign. This demo did not email anyone."

---

## Cut list (edit)

| Clip | Max length |
|------|------------|
| Doctor PASS | 15s |
| Smoke PASS | 20s |
| Demo status 100 | 30s |
| Open board-pack zip contents | 30s |
| Compliance PASS | 15s |
| End card: DRAFT tools / seeking VT collaboration (no partnership claim) | 10s |

---

## Do not film

- Live secrets / API keys  
- Real founder bank data (use demo company only)  
- Claims of existing VT partnership  

---

## After filming

1. Store video privately (Drive / OneDrive - not public git).  
2. Log RDTI hours if the work was R&D experiment (tooling/process).  
3. Optional: link private URL in investor teaser when human chooses.  
