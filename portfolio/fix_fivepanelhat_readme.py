#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess

p = Path(r"C:\Users\Admin\source\portfolio-work\fivepanelhat\README.md")
t = p.read_text(encoding="utf-8", errors="replace")

fixes = [
    ("M\u00c4ori", "Maori"),
    ("MÄori", "Maori"),
    ("\u00e2\u0080\u0094", "-"),
    ("\u00e2\u0080\u0093", "-"),
    ("\u00e2\u0080\u0099", "'"),
    ("\u00e2\u0080\u009c", '"'),
    ("\u00e2\u0080\u009d", '"'),
    ("\u00e2\u0080\u00a6", "..."),
    ("\u00e2\u0089\u00a5", ">="),
    ("\u00e2\u0089\u00a4", "<="),
    ("\ufffd", ""),
    ("Â", ""),
    ("7089%", "70-89%"),
]
for a, b in fixes:
    t = t.replace(a, b)

t = re.sub(r"â[^\w\s]{0,6}\s*", "", t)
t = re.sub(r"ð[^\s]{1,10}\s*", "", t)

snippet = Path(
    r"C:\Users\Admin\source\NZ-Start-Up\portfolio\congruence-pack\README_SNIPPET.md"
).read_text(encoding="utf-8").strip()
if "BEGIN CAT_CONGRUENCE_SNIPPET" in t:
    t = re.sub(
        r"(?s)<!-- BEGIN CAT_CONGRUENCE_SNIPPET -->.*?<!-- END CAT_CONGRUENCE_SNIPPET -->",
        snippet,
        t,
    )

t = t.replace("\r\n", "\n").replace("\r", "\n")
if not t.endswith("\n"):
    t += "\n"
p.write_bytes(t.encode("utf-8"))

non = set(c for c in t if ord(c) > 127)
print("remaining unique non-ascii:", non)
for i, line in enumerate(t.splitlines(), 1):
    if any(ord(c) > 127 for c in line):
        print(i, line[:120])

repo = Path(r"C:\Users\Admin\source\portfolio-work\fivepanelhat")
subprocess.run(["git", "add", "README.md"], cwd=repo, check=False)
st = subprocess.run(
    ["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True
)
if st.stdout.strip():
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "fix: clean README mojibake and ASCII-safe portfolio snippet",
        ],
        cwd=repo,
        check=False,
    )
    subprocess.run(["git", "push", "origin", "main"], cwd=repo, check=False)
    print("pushed fivepanelhat")
else:
    print("no changes")
