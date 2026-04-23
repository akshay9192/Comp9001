from __future__ import annotations

import pygame

import config


class Boss:
    def __init__(self, name: str, x: int, y: int, week: int):
        self.name = name
        self.rect = pygame.Rect(x, y, 64, 64)
        self.max_hp = 30 + week * 6
        self.hp = self.max_hp
        self.alive = True
        self.dir = 1

    def update(self) -> None:
        if not self.alive:
            return
        self.rect.x += 2 * self.dir
        if self.rect.x < 620 or self.rect.x > 860:
            self.dir *= -1

    def take_hit(self, amount: int) -> bool:
        if not self.alive:
            return False
        self.hp -= max(1, amount)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return True
        return False

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        if not self.alive:
            return
        r = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, config.COLORS["boss"], r, border_radius=8)
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (60, 20, 20), (r.x, r.y - 12, r.width, 8))
        pygame.draw.rect(screen, (240, 90, 90), (r.x, r.y - 12, int(r.width * ratio), 8))
