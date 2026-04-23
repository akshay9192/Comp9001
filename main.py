"""Repository-level launcher for the COMP9001 pygame project."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent / "comp9001_wizard_game"
sys.path.insert(0, str(PROJECT_DIR))

from main import main as game_main


if __name__ == "__main__":
    asyncio.run(game_main())
