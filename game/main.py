"""Async entry point for COMP9001 13-week educational platformer (pygame + pygbag friendly)."""

from __future__ import annotations

import asyncio

import pygame

import config
from engine import GameEngine


async def main() -> None:
    pygame.init()
    pygame.display.set_caption("COMP9001 Knowledge Castle")
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    engine = GameEngine(screen)

    while engine.running:
        await engine.tick()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
