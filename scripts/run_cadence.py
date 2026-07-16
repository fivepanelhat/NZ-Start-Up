#!/usr/bin/env python3
"""Thin launcher - real runner lives in ~/.nz-startup/run_cadence.py (T5)."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

target = Path.home() / ".nz-startup" / "run_cadence.py"
if not target.is_file():
 # bootstrap via package
 from nz_startup.schedule import _runner_script

 target = _runner_script()
sys.argv[0] = str(target)
runpy.run_path(str(target), run_name="__main__")
