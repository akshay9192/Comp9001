"""Enemy hierarchy representing conceptual coding errors."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

import config


@dataclass
class EnemyConfig:
    color_key: str
    speed: float
    damage: int
    xp_reward: int


ENEMY_TYPES: dict[str, EnemyConfig] = {
    "syntax_bug": EnemyConfig("enemy_syntax", 1.5, 8, 4),
    "stress_monster": EnemyConfig("enemy_stress", 2.2, 10, 5),
    "logic_ghost": EnemyConfig("enemy_logic", 1.8, 9, 5),
}


class Enemy:
    def __init__(self, x: int, y: int, enemy_type: str) -> None:
        self.rect = pygame.Rect(x, y, 28, 28)
        self.enemy_type = enemy_type if enemy_type in ENEMY_TYPES else "syntax_bug"
        self.cfg = ENEMY_TYPES[self.enemy_type]
        self.direction = 1
        self.patrol_min = x - 80
        self.patrol_max = x + 80
        self.alive = True

    def update(self) -> None:
        if not self.alive:
            return
        self.rect.x += int(self.cfg.speed * self.direction)
        if self.rect.x <= self.patrol_min or self.rect.x >= self.patrol_max:
            self.direction *= -1

    def draw(self, screen: pygame.Surface, camera_x: int) -> None:
        if not self.alive:
            return
        color = config.COLORS[self.cfg.color_key]
        pygame.draw.circle(screen, color, (self.rect.centerx - camera_x, self.rect.centery), 14)

    def on_player_collision(self) -> tuple[int, int]:
        """Return (damage_to_player, xp_reward_for_player_if_defeated)."""
        self.alive = False
        return self.cfg.damage, self.cfg.xp_reward
