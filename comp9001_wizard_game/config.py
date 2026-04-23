"""Configuration and player profile state for the COMP9001 Wizard RPG."""

from __future__ import annotations

from typing import Dict

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Class inequality starter stats (balanced so every path is completable).
CLASS_STATS: Dict[str, Dict[str, int]] = {
    "wealthy": {"xp": 90, "time": 95},
    "middle": {"xp": 72, "time": 75},
    "lower": {"xp": 60, "time": 62},
}

BACKGROUND_LABELS = {
    "1": "wealthy",
    "2": "middle",
    "3": "lower",
}

BACKGROUND_NAMES = {
    "wealthy": "Wealthy",
    "middle": "Middle-income",
    "lower": "Lower-income",
}

# Mutable player profile that gets filled at runtime.
PLAYER_PROFILE = {
    "name": "",
    "course": "COMP9001",
    "background": "middle",
}


def set_player_profile(name: str, course: str, background: str) -> dict:
    """Set player data in a single place and return the updated profile."""
    PLAYER_PROFILE["name"] = name.strip() or "Student"
    PLAYER_PROFILE["course"] = course.strip() or "COMP9001"
    PLAYER_PROFILE["background"] = background if background in CLASS_STATS else "middle"
    return PLAYER_PROFILE


def get_starting_stats(background: str) -> dict:
    """Return a copy of starter stats for the selected background."""
    chosen = background if background in CLASS_STATS else "middle"
    return CLASS_STATS[chosen].copy()
