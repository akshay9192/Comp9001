"""Random event system for the weekly simulation."""

from __future__ import annotations

import random
from typing import Dict, List

Event = Dict[str, object]


def _event_pool_for_background(background: str) -> List[Event]:
    """Build weighted event pool by adding repeated entries for likely events."""
    common_events: List[Event] = [
        {
            "name": "Group study session",
            "description": "You joined a group study session in the library.",
            "effects": {"xp": 10, "time": -6},
        },
        {
            "name": "Laptop broke",
            "description": "Your laptop crashed before assignment practice.",
            "effects": {"xp": -4, "time": -12},
        },
        {
            "name": "Campus mentor workshop",
            "description": "A free coding workshop gave you practical examples.",
            "effects": {"xp": 9, "time": -5},
        },
    ]

    wealthy_events: List[Event] = [
        {
            "name": "Private tutor available",
            "description": "You hired a private tutor for one focused evening.",
            "effects": {"xp": 15, "time": -7},
        }
    ]

    middle_events: List[Event] = [
        {
            "name": "Family commitment",
            "description": "You handled home responsibilities after class.",
            "effects": {"xp": -2, "time": -9},
        }
    ]

    lower_events: List[Event] = [
        {
            "name": "Extra work shift",
            "description": "You took an extra shift to cover living costs.",
            "effects": {"xp": -3, "time": -14},
        },
        {
            "name": "Community scholarship",
            "description": "A small grant reduced stress and gave you focused study time.",
            "effects": {"xp": 8, "time": -3},
        },
    ]

    pool = common_events.copy()
    if background == "wealthy":
        pool += wealthy_events * 3 + middle_events + lower_events[:1]
    elif background == "middle":
        pool += middle_events * 2 + lower_events + wealthy_events
    else:
        pool += lower_events * 3 + middle_events * 2 + wealthy_events

    return pool


def get_random_event(background: str) -> Event:
    """Return one event with weighted probability by socioeconomic background."""
    pool = _event_pool_for_background(background)
    return random.choice(pool)
