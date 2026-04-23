"""World generation helpers for level geometry and object placement."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from enemies import Enemy


@dataclass
class WorldData:
    platforms: list[pygame.Rect]
    enemies: list[Enemy]
    goal_rect: pygame.Rect
    spawn_point: tuple[int, int]


def generate_platforms(mechanic_type: str) -> list[pygame.Rect]:
    base = [
        pygame.Rect(0, 500, 1400, 40),
        pygame.Rect(200, 430, 150, 20),
        pygame.Rect(430, 380, 140, 20),
        pygame.Rect(650, 330, 170, 20),
        pygame.Rect(910, 290, 130, 20),
    ]

    if mechanic_type == "conditional_paths":
        base += [pygame.Rect(300, 300, 120, 16), pygame.Rect(500, 250, 120, 16), pygame.Rect(780, 220, 120, 16)]
    elif mechanic_type == "loop_platforms":
        base += [pygame.Rect(250 + i * 120, 260 - (i % 2) * 40, 100, 16) for i in range(7)]
    elif mechanic_type == "recursion_stairs":
        base += [pygame.Rect(220 + i * 80, 460 - i * 26, 90, 16) for i in range(8)]
    elif mechanic_type == "file_keys":
        base += [pygame.Rect(340, 200, 110, 16), pygame.Rect(780, 170, 140, 16)]
    elif mechanic_type == "revision_castle":
        base += [pygame.Rect(260 + i * 95, 250 + ((-1) ** i) * 35, 90, 16) for i in range(8)]

    return base


def generate_enemies(enemy_types: list[str], week_number: int) -> list[Enemy]:
    enemies: list[Enemy] = []
    spacing = 140
    x = 280
    y = 470
    for idx in range(5 + week_number // 2):
        enemy_type = enemy_types[idx % len(enemy_types)] if enemy_types else "syntax_bug"
        enemies.append(Enemy(x + idx * spacing, y, enemy_type))
    return enemies


def build_world(week_data: dict) -> WorldData:
    platforms = generate_platforms(week_data["mechanic_type"])
    enemies = generate_enemies(week_data.get("enemy_types", []), week_data["week"])
    goal_rect = pygame.Rect(1220, 230, 42, 60)
    spawn_point = (90, 430)
    return WorldData(platforms=platforms, enemies=enemies, goal_rect=goal_rect, spawn_point=spawn_point)
