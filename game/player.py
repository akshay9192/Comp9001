"""Player entity and movement/character progression."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

import config


@dataclass
class PlayerStats:
    xp: int = 0
    stamina: float = float(config.PLAYER_MAX_STAMINA)
    hp: int = config.PLAYER_MAX_HP


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, 36, 48)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False
        self.stats = PlayerStats()

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.vel_x = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -config.PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = config.PLAYER_SPEED

    def jump(self) -> None:
        if self.on_ground and self.stats.stamina >= 2:
            self.vel_y = config.JUMP_FORCE
            self.on_ground = False
            self.stats.stamina = max(0, self.stats.stamina - 2)

    def apply_gravity(self) -> None:
        self.vel_y += config.GRAVITY
        if self.vel_y > 14:
            self.vel_y = 14

    def update(self, platforms: list[pygame.Rect]) -> None:
        self.apply_gravity()

        self.rect.x += int(self.vel_x)
        self._collide_horizontal(platforms)

        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self._collide_vertical(platforms)

        if abs(self.vel_x) > 0:
            self.stats.stamina = max(0, self.stats.stamina - 0.04)
        else:
            self.stats.stamina = min(config.PLAYER_MAX_STAMINA, self.stats.stamina + 0.08)

    def _collide_horizontal(self, platforms: list[pygame.Rect]) -> None:
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.rect.right = platform.left
                elif self.vel_x < 0:
                    self.rect.left = platform.right

    def _collide_vertical(self, platforms: list[pygame.Rect]) -> None:
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0

    def reward_xp(self, amount: int) -> None:
        self.stats.xp += max(0, amount)

    def damage(self, amount: int) -> None:
        self.stats.hp = max(0, self.stats.hp - max(0, amount))
        self.stats.stamina = max(0, self.stats.stamina - amount * 0.2)

    def reset_position(self, x: int, y: int) -> None:
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
