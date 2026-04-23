from __future__ import annotations

from dataclasses import dataclass

import pygame

from enemies import Enemy


@dataclass
class WorldData:
    platforms: list[pygame.Rect]
    enemies: list[Enemy]
    goal: pygame.Rect
    spawn: tuple[int, int]


def generate_platforms(mechanic: str) -> list[pygame.Rect]:
    platforms = [
        pygame.Rect(0, 500, 1400, 40),
        pygame.Rect(200, 430, 150, 20),
        pygame.Rect(430, 380, 140, 20),
        pygame.Rect(650, 330, 170, 20),
        pygame.Rect(910, 290, 130, 20),
    ]
    if mechanic == "conditional_paths":
        platforms += [pygame.Rect(300, 300, 120, 16), pygame.Rect(500, 250, 120, 16), pygame.Rect(780, 220, 120, 16)]
    elif mechanic == "loop_platforms":
        platforms += [pygame.Rect(250 + i * 120, 260 - (i % 2) * 40, 100, 16) for i in range(7)]
    elif mechanic == "recursion_stairs":
        platforms += [pygame.Rect(220 + i * 80, 460 - i * 26, 90, 16) for i in range(8)]
    elif mechanic == "file_keys":
        platforms += [pygame.Rect(340, 200, 110, 16), pygame.Rect(780, 170, 140, 16)]
    elif mechanic == "revision_castle":
        platforms += [pygame.Rect(260 + i * 95, 250 + ((-1) ** i) * 35, 90, 16) for i in range(8)]
    return platforms


def generate_enemies(enemy_types: list[str], week: int) -> list[Enemy]:
    out = []
    for i in range(5 + week // 2):
        t = enemy_types[i % len(enemy_types)] if enemy_types else "syntax_bug"
        out.append(Enemy(280 + i * 140, 470, t))
    return out


def build_world(week_data: dict) -> WorldData:
    return WorldData(
        platforms=generate_platforms(week_data["mechanic_type"]),
        enemies=generate_enemies(week_data.get("enemy_types", []), week_data["week"]),
        goal=pygame.Rect(1220, 230, 42, 60),
        spawn=(90, 430),
    )
