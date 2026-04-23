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
    def __init__(self, x: int, y: int):
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

    def update(self, platforms: list[pygame.Rect]) -> None:
        self.vel_y += config.GRAVITY
        self.vel_y = min(self.vel_y, 14)

        self.rect.x += int(self.vel_x)
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_x > 0:
                    self.rect.right = p.left
                elif self.vel_x < 0:
                    self.rect.left = p.right

        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.bottom
                    self.vel_y = 0

        if abs(self.vel_x) > 0:
            self.stats.stamina = max(0, self.stats.stamina - 0.04)
        else:
            self.stats.stamina = min(config.PLAYER_MAX_STAMINA, self.stats.stamina + 0.08)

    def reward_xp(self, amount: int) -> None:
        self.stats.xp += max(0, amount)

    def damage(self, amount: int) -> None:
        self.stats.hp = max(0, self.stats.hp - max(0, amount))

    def reset_position(self, x: int, y: int) -> None:
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
