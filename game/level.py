"""Level orchestration for weekly gameplay segments."""

from __future__ import annotations

import pygame

from bosses import Boss
from world import WorldData, build_world


class Level:
    def __init__(self, week_data: dict):
        self.week_data = week_data
        self.world: WorldData = build_world(week_data)
        self.boss_spawned = False
        self.boss = Boss(week_data["boss_name"], 760, 430, week_data["week"])
        self.boss_active = False
        self.completed = False

    def update(self) -> None:
        for enemy in self.world.enemies:
            enemy.update()
        if self.boss_active:
            self.boss.update()

    def maybe_activate_boss(self, player_rect: pygame.Rect) -> bool:
        if self.boss_active:
            return False
        if player_rect.colliderect(self.world.goal_rect):
            self.boss_active = True
            return True
        return False

    def draw(self, screen: pygame.Surface, camera_x: int, palette: dict[str, tuple[int, int, int]]) -> None:
        for platform in self.world.platforms:
            screen_rect = pygame.Rect(platform.x - camera_x, platform.y, platform.width, platform.height)
            pygame.draw.rect(screen, palette["platform"], screen_rect)

        pygame.draw.rect(
            screen,
            palette["goal"],
            pygame.Rect(
                self.world.goal_rect.x - camera_x,
                self.world.goal_rect.y,
                self.world.goal_rect.width,
                self.world.goal_rect.height,
            ),
            border_radius=6,
        )

        for enemy in self.world.enemies:
            enemy.draw(screen, camera_x)

        if self.boss_active:
            self.boss.draw(screen, camera_x)
