from __future__ import annotations

import pygame

from bosses import Boss
from world import WorldData, build_world


class Level:
    def __init__(self, week_data: dict):
        self.week_data = week_data
        self.world: WorldData = build_world(week_data)
        self.boss = Boss(week_data["boss_name"], 760, 430, week_data["week"])
        self.boss_active = False

    def update(self) -> None:
        for enemy in self.world.enemies:
            enemy.update()
        if self.boss_active:
            self.boss.update()

    def maybe_activate_boss(self, player_rect: pygame.Rect) -> bool:
        if self.boss_active:
            return False
        if player_rect.colliderect(self.world.goal):
            self.boss_active = True
            return True
        return False

    def draw(self, screen: pygame.Surface, camera_x: int, colors: dict[str, tuple[int, int, int]]) -> None:
        for p in self.world.platforms:
            pygame.draw.rect(screen, colors["platform"], pygame.Rect(p.x - camera_x, p.y, p.width, p.height))

        pygame.draw.rect(
            screen,
            colors["goal"],
            pygame.Rect(self.world.goal.x - camera_x, self.world.goal.y, self.world.goal.width, self.world.goal.height),
            border_radius=6,
        )

        for e in self.world.enemies:
            e.draw(screen, camera_x)
        if self.boss_active:
            self.boss.draw(screen, camera_x)
