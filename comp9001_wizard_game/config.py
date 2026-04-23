"""Shared configuration for the 13-week COMP9001 platformer RPG."""

from __future__ import annotations

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
GRAVITY = 0.62

PLAYER_SPEED = 5.0
JUMP_FORCE = -12.5
PLAYER_MAX_HP = 100
PLAYER_MAX_STAMINA = 100

QUIZ_QUESTIONS_PER_WEEK = 10
QUIZ_PASS_SCORE = 7
TOTAL_WEEKS = 13

COLORS = {
    "platform": (72, 92, 120),
    "player": (255, 222, 130),
    "enemy_syntax": (220, 85, 85),
    "enemy_stress": (210, 130, 70),
    "enemy_logic": (155, 95, 225),
    "boss": (240, 60, 140),
    "text": (236, 236, 236),
    "panel": (15, 18, 30),
    "xp": (85, 210, 120),
    "stamina": (90, 170, 245),
    "goal": (255, 250, 145),
}

WEEK_BG_COLORS = [
    (30, 40, 64), (24, 62, 78), (52, 45, 88), (30, 74, 68), (80, 58, 39),
    (44, 76, 36), (64, 49, 80), (38, 60, 92), (77, 40, 68), (26, 68, 86),
    (66, 58, 40), (84, 48, 48), (50, 50, 50),
]

MECHANIC_HINTS = {
    "intro_jumps": "Jump timing matters more than speed.",
    "variable_gates": "Watch your resources and choose safely.",
    "conditional_paths": "Observe paths before committing.",
    "advanced_conditionals": "Nested choices can trap rushed players.",
    "loop_platforms": "Patterns repeat; learn the rhythm.",
    "function_switches": "Order matters—trigger in sequence.",
    "collection_waves": "Manage grouped threats efficiently.",
    "object_allies": "Use entity interactions to your advantage.",
    "file_keys": "Find required keys before doors.",
    "flow_gauntlet": "Adjust strategy for each segment.",
    "test_trials": "Validate assumptions at checkpoints.",
    "recursion_stairs": "Solve one layer, then the next.",
    "revision_castle": "Combine all skills under pressure.",
}
