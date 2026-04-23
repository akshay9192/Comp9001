"""Boss enemies representing week concept masters."""

from __future__ import annotations

import pygame

import config


class Boss:
    def __init__(self, name: str, x: int, y: int, week_number: int) -> None:
        self.name = name
        self.week_number = week_number
        self.rect = pygame.Rect(x, y, 64, 64)
        self.max_hp = 30 + week_number * 6
        self.hp = self.max_hp
        self.direction = 1
        self.alive = True

    def update(self) -> None:
        if not self.alive:
            return
        self.rect.x += 2 * self.direction
        if self.rect.x < 620 or self.rect.x > 860:
            self.direction *= -1

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        if not self.alive:
            return
        screen_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, config.COLORS["boss"], screen_rect, border_radius=8)

        hp_ratio = self.hp / self.max_hp if self.max_hp else 0
        pygame.draw.rect(screen, (60, 20, 20), (screen_rect.x, screen_rect.y - 12, screen_rect.width, 8))
        pygame.draw.rect(
            screen,
            (240, 90, 90),
            (screen_rect.x, screen_rect.y - 12, int(screen_rect.width * hp_ratio), 8),
        )

    def take_hit(self, amount: int) -> bool:
        if not self.alive:
            return False
        self.hp -= max(1, amount)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return True
        return False
