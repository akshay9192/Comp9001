"""Global configuration constants for the COMP9001 platformer."""

from __future__ import annotations

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
GRAVITY = 0.65

PLAYER_SPEED = 5.2
JUMP_FORCE = -12.8
PLAYER_MAX_HP = 100
PLAYER_MAX_STAMINA = 100

QUIZ_QUESTIONS_PER_WEEK = 10
QUIZ_PASS_SCORE = 7
TOTAL_WEEKS = 13

COLORS = {
    "bg": (25, 28, 40),
    "platform": (68, 83, 115),
    "player": (255, 220, 120),
    "enemy_syntax": (220, 80, 80),
    "enemy_stress": (200, 120, 60),
    "enemy_logic": (150, 90, 220),
    "boss": (240, 60, 140),
    "text": (235, 235, 235),
    "panel": (16, 18, 28),
    "xp": (80, 210, 120),
    "stamina": (90, 170, 245),
    "goal": (255, 255, 150),
}

WEEK_BG_COLORS = [
    (30, 40, 64),
    (22, 62, 75),
    (52, 45, 88),
    (28, 72, 65),
    (78, 56, 37),
    (45, 74, 35),
    (64, 49, 79),
    (40, 62, 94),
    (78, 41, 70),
    (26, 69, 89),
    (68, 58, 40),
    (84, 49, 49),
    (52, 52, 52),
]

MECHANIC_THEME = {
    "intro_jumps": "basic jumping and timing",
    "variable_gates": "resource pickups and stat gates",
    "conditional_paths": "branching route selection",
    "advanced_conditionals": "risk/reward switch routes",
    "loop_platforms": "repeating moving platform pattern",
    "function_switches": "trigger order puzzle",
    "collection_waves": "group enemy handling",
    "object_allies": "support drones and interactions",
    "file_keys": "door and key retrieval",
    "flow_gauntlet": "timed flow-control rooms",
    "test_trials": "checkpoint challenge rounds",
    "recursion_stairs": "self-similar step obstacles",
    "revision_castle": "mixed mastery gauntlet",
}
