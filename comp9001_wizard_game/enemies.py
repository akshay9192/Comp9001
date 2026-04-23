from __future__ import annotations

from dataclasses import dataclass

import pygame

import config


@dataclass
class EnemySpec:
    color: str
    speed: float
    damage: int
    xp: int


ENEMY_SPECS = {
    "syntax_bug": EnemySpec("enemy_syntax", 1.5, 8, 4),
    "stress_monster": EnemySpec("enemy_stress", 2.1, 10, 5),
    "logic_ghost": EnemySpec("enemy_logic", 1.8, 9, 5),
}


class Enemy:
    def __init__(self, x: int, y: int, enemy_type: str):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.spec = ENEMY_SPECS.get(enemy_type, ENEMY_SPECS["syntax_bug"])
        self.alive = True
        self.dir = 1
        self.left = x - 80
        self.right = x + 80

    def update(self) -> None:
        if not self.alive:
            return
        self.rect.x += int(self.spec.speed * self.dir)
        if self.rect.x <= self.left or self.rect.x >= self.right:
            self.dir *= -1

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        if self.alive:
            pygame.draw.circle(screen, config.COLORS[self.spec.color], (self.rect.centerx - camera_x, self.rect.centery), 14)

    def collide_player(self) -> tuple[int, int]:
        self.alive = False
        return self.spec.damage, self.spec.xp
