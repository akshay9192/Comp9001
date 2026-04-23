from __future__ import annotations

from typing import Iterable

import pygame

import config


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 22)
        self.small = pygame.font.SysFont("arial", 18)
        self.title = pygame.font.SysFont("arial", 28, bold=True)

    def draw_hud(self, screen: pygame.Surface, week: int, topic: str, xp: int, stamina: float, hp: int) -> None:
        pygame.draw.rect(screen, config.COLORS["panel"], (0, 0, config.SCREEN_WIDTH, 80))
        pygame.draw.rect(screen, (60, 60, 60), (20, 42, 220, 16))
        pygame.draw.rect(screen, config.COLORS["xp"], (20, 42, int(220 * min(1, xp / 400)), 16))
        screen.blit(self.small.render(f"XP: {xp}", True, config.COLORS["text"]), (22, 18))

        pygame.draw.rect(screen, (60, 60, 60), (270, 42, 220, 16))
        pygame.draw.rect(screen, config.COLORS["stamina"], (270, 42, int(220 * max(0, min(1, stamina / config.PLAYER_MAX_STAMINA))), 16))
        screen.blit(self.small.render(f"Stamina: {int(stamina)}", True, config.COLORS["text"]), (272, 18))

        screen.blit(self.small.render(f"HP: {hp}", True, config.COLORS["text"]), (520, 18))
        screen.blit(self.small.render(f"Week {week}: {topic}", True, config.COLORS["text"]), (520, 42))

    def draw_dialogue(self, screen: pygame.Surface, text: str) -> None:
        pygame.draw.rect(screen, config.COLORS["panel"], (20, config.SCREEN_HEIGHT - 110, config.SCREEN_WIDTH - 40, 90), border_radius=8)
        y = config.SCREEN_HEIGHT - 95
        for line in self._wrap(text, config.SCREEN_WIDTH - 80)[:3]:
            screen.blit(self.font.render(line, True, config.COLORS["text"]), (35, y))
            y += 26

    def draw_objectives(self, screen: pygame.Surface, objectives: Iterable[str]) -> None:
        y = 88
        for obj in list(objectives)[:2]:
            screen.blit(self.small.render(f"Objective: {obj}", True, (200, 210, 230)), (20, y))
            y += 22

    def draw_quiz(self, screen: pygame.Surface, q: dict, num: int) -> None:
        overlay = pygame.Surface((config.SCREEN_WIDTH - 120, config.SCREEN_HEIGHT - 140), pygame.SRCALPHA)
        overlay.fill((10, 10, 16, 235))
        screen.blit(overlay, (60, 70))
        screen.blit(self.title.render(f"Armin Quiz Gate - Q{num}/10", True, config.COLORS["text"]), (84, 92))

        y = 132
        for line in self._wrap(q["question"], config.SCREEN_WIDTH - 180):
            screen.blit(self.font.render(line, True, config.COLORS["text"]), (84, y))
            y += 28
        y += 12
        for key in ["A", "B", "C", "D"]:
            screen.blit(self.font.render(f"{key}) {q['options'][key]}", True, (245, 220, 130)), (100, y))
            y += 34

    def _wrap(self, text: str, width: int) -> list[str]:
        words = text.split()
        lines = []
        current = ""
        for w in words:
            trial = f"{current} {w}".strip()
            if self.font.size(trial)[0] <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines
