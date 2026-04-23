"""Entry point for the COMP9001 Wizard RPG (desktop + pygbag friendly)."""

from __future__ import annotations

import asyncio

import pygame

import config
from game import Game


async def main() -> None:
    """Initialize pygame and run the async game loop."""
    pygame.init()
    pygame.display.set_caption("COMP9001 Wizard Game")
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    game = Game(screen)
    await game.run()

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
