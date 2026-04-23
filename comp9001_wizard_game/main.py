"""Async entrypoint for the 13-week COMP9001 platformer RPG."""

from __future__ import annotations

import asyncio

import pygame

import config
from game import Game


async def main() -> None:
    pygame.init()
    pygame.display.set_caption("COMP9001 Knowledge Castle")
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    game = Game(screen)
    while game.running:
        await game.tick()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
