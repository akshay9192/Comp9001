"""UI rendering components for HUD, dialogue, and quiz overlays."""

from __future__ import annotations

from typing import Iterable

import pygame

import config


class UI:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 28, bold=True)

    def draw_hud(self, screen: pygame.Surface, week_number: int, topic: str, xp: int, stamina: float, hp: int) -> None:
        pygame.draw.rect(screen, config.COLORS["panel"], (0, 0, config.SCREEN_WIDTH, 80))

        xp_ratio = min(1.0, xp / 400)
        stamina_ratio = max(0.0, min(1.0, stamina / config.PLAYER_MAX_STAMINA))

        pygame.draw.rect(screen, (60, 60, 60), (20, 42, 220, 16))
        pygame.draw.rect(screen, config.COLORS["xp"], (20, 42, int(220 * xp_ratio), 16))
        screen.blit(self.small_font.render(f"XP: {xp}", True, config.COLORS["text"]), (22, 18))

        pygame.draw.rect(screen, (60, 60, 60), (270, 42, 220, 16))
        pygame.draw.rect(screen, config.COLORS["stamina"], (270, 42, int(220 * stamina_ratio), 16))
        screen.blit(self.small_font.render(f"Stamina: {int(stamina)}", True, config.COLORS["text"]), (272, 18))

        hp_text = self.small_font.render(f"HP: {hp}", True, config.COLORS["text"])
        week_text = self.small_font.render(f"Week {week_number}: {topic}", True, config.COLORS["text"])
        screen.blit(hp_text, (520, 18))
        screen.blit(week_text, (520, 42))

    def draw_dialogue(self, screen: pygame.Surface, text: str) -> None:
        pygame.draw.rect(screen, config.COLORS["panel"], (20, config.SCREEN_HEIGHT - 110, config.SCREEN_WIDTH - 40, 90), border_radius=8)
        wrapped = self._wrap(text, self.font, config.SCREEN_WIDTH - 80)
        y = config.SCREEN_HEIGHT - 95
        for line in wrapped[:3]:
            screen.blit(self.font.render(line, True, config.COLORS["text"]), (35, y))
            y += 26

    def draw_quiz_overlay(self, screen: pygame.Surface, question_data: dict, question_number: int) -> None:
        overlay = pygame.Surface((config.SCREEN_WIDTH - 120, config.SCREEN_HEIGHT - 140), pygame.SRCALPHA)
        overlay.fill((10, 10, 16, 235))
        screen.blit(overlay, (60, 70))

        q_title = self.title_font.render(f"Armin Quiz Gate - Q{question_number}/10", True, config.COLORS["text"])
        screen.blit(q_title, (84, 92))

        prompt_lines = self._wrap(question_data["question"], self.font, config.SCREEN_WIDTH - 180)
        y = 132
        for line in prompt_lines:
            screen.blit(self.font.render(line, True, config.COLORS["text"]), (84, y))
            y += 28

        y += 12
        for key in ["A", "B", "C", "D"]:
            option_text = f"{key}) {question_data['options'][key]}"
            screen.blit(self.font.render(option_text, True, (245, 220, 130)), (100, y))
            y += 34

        hint = self.small_font.render("Press A, B, C, or D to answer.", True, (190, 200, 220))
        screen.blit(hint, (84, config.SCREEN_HEIGHT - 102))

    def _wrap(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            proposal = f"{current} {word}".strip()
            if font.size(proposal)[0] <= max_width:
                current = proposal
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw_objectives(self, screen: pygame.Surface, objectives: Iterable[str]) -> None:
        y = 88
        for objective in list(objectives)[:2]:
            line = self.small_font.render(f"Objective: {objective}", True, (200, 210, 230))
            screen.blit(line, (20, y))
            y += 22
