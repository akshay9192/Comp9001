"""Pygame UI helpers for text rendering, choice input, and text entry."""

from __future__ import annotations

import asyncio
from typing import Dict, Iterable, List, Optional, Tuple

import pygame

from config import WINDOW_HEIGHT, WINDOW_WIDTH


class UIManager:
    """Draws text scenes and provides async input helpers for pygame/pygbag."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.title_font = pygame.font.SysFont("arial", 34, bold=True)
        self.body_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 20)

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        words = text.split()
        lines: List[str] = []
        current = ""

        for word in words:
            trial = f"{current} {word}".strip()
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines or [""]

    def draw_scene(
        self,
        title: str,
        lines: Iterable[str],
        choices: Dict[str, str],
        stats_text: str,
        background_color: Tuple[int, int, int],
    ) -> None:
        """Render one complete scene with title, body text, choices, and footer stats."""
        self.screen.fill(background_color)

        title_surface = self.title_font.render(title, True, (255, 255, 255))
        self.screen.blit(title_surface, (30, 25))

        wrapped_lines: List[str] = []
        for raw_line in lines:
            wrapped_lines.extend(self._wrap_text(raw_line, self.body_font, WINDOW_WIDTH - 60))
            wrapped_lines.append("")

        choice_block_height = max(1, len(choices)) * 34 + 20
        choice_start_y = WINDOW_HEIGHT - choice_block_height - 90
        max_text_rows = max(3, int((choice_start_y - 95) / 30))

        trimmed = wrapped_lines[:max_text_rows]
        if len(wrapped_lines) > max_text_rows and trimmed:
            trimmed[-1] = "..."

        y = 90
        for line in trimmed:
            if line:
                line_surface = self.body_font.render(line, True, (240, 240, 240))
                self.screen.blit(line_surface, (30, y))
            y += 30

        y = choice_start_y
        for key, text in choices.items():
            choice_line = f"{key}. {text}"
            choice_surface = self.body_font.render(choice_line, True, (255, 230, 160))
            self.screen.blit(choice_surface, (50, y))
            y += 34

        footer = self.small_font.render(stats_text, True, (180, 220, 255))
        hint = self.small_font.render("Use number keys to choose.", True, (200, 200, 200))
        self.screen.blit(footer, (30, WINDOW_HEIGHT - 50))
        self.screen.blit(hint, (WINDOW_WIDTH - 275, WINDOW_HEIGHT - 50))

        pygame.display.flip()

    def draw_text_prompt(
        self,
        title: str,
        prompt: str,
        current_text: str,
        helper_text: str,
        background_color: Tuple[int, int, int],
    ) -> None:
        """Render a text input scene for setup screens."""
        self.screen.fill(background_color)
        self.screen.blit(self.title_font.render(title, True, (255, 255, 255)), (30, 30))

        prompt_lines = self._wrap_text(prompt, self.body_font, WINDOW_WIDTH - 60)
        y = 120
        for line in prompt_lines:
            self.screen.blit(self.body_font.render(line, True, (240, 240, 240)), (30, y))
            y += 34

        pygame.draw.rect(self.screen, (235, 235, 235), (30, y + 10, WINDOW_WIDTH - 60, 52), border_radius=8)
        pygame.draw.rect(self.screen, (50, 50, 60), (34, y + 14, WINDOW_WIDTH - 68, 44), border_radius=6)

        display = current_text if current_text else "_"
        self.screen.blit(self.body_font.render(display, True, (255, 255, 200)), (44, y + 23))
        self.screen.blit(self.small_font.render(helper_text, True, (200, 200, 200)), (30, y + 80))
        pygame.display.flip()

    async def wait_for_choice(self, valid_choices: Iterable[str]) -> Optional[str]:
        """Wait asynchronously for a valid number key press or window close."""
        valid_set = set(valid_choices)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.unicode in valid_set:
                    return event.unicode
            await asyncio.sleep(0)

    async def prompt_text(
        self,
        title: str,
        prompt: str,
        helper_text: str,
        default_text: str = "",
        max_len: int = 24,
        background_color: Tuple[int, int, int] = (25, 25, 45),
    ) -> Optional[str]:
        """Get short text input asynchronously; returns None if the window is closed."""
        text = default_text

        while True:
            self.draw_text_prompt(title, prompt, text, helper_text, background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return text.strip() or default_text
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if event.unicode.isprintable() and len(text) < max_len:
                            text += event.unicode
            await asyncio.sleep(0)
