"""Repository-level launcher for the COMP9001 pygame project."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent / "comp9001_wizard_game"
TARGET = PROJECT_DIR / "main.py"

if __name__ == "__main__":
    sys.path.insert(0, str(PROJECT_DIR))
    runpy.run_path(str(TARGET), run_name="__main__")
