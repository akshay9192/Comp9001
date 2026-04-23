"""Core game engine orchestrating gameplay, mentors, bosses, and quiz gates."""

from __future__ import annotations

import json
from pathlib import Path

import pygame

import config
from level import Level
from mentor import ArminGatekeeper, MentorNPC
from player import Player
from quiz_engine import QuizEngine
from ui import UI


class GameEngine:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ui = UI()

        self.weeks_data = self._load_weeks_data()
        self.week_index = 0

        self.player = Player(80, 400)
        self.level = Level(self.weeks_data[self.week_index])
        self.quiz_engine = QuizEngine()

        self.leon = MentorNPC()
        self.armin = ArminGatekeeper()

        self.state = "gameplay"  # gameplay | preboss | quiz | week_result | complete
        self.dialogue = self.leon.hint_for_mechanic(self.current_week_data["mechanic_type"])
        self.quiz_message = ""
        self.running = True

    @property
    def current_week_data(self) -> dict:
        return self.weeks_data[self.week_index]

    def _load_weeks_data(self) -> list[dict]:
        data_path = Path(__file__).resolve().parent / "data" / "weeks.json"
        with data_path.open("r", encoding="utf-8") as file:
            weeks = json.load(file)

        if len(weeks) < config.TOTAL_WEEKS:
            raise ValueError(f"weeks.json must contain {config.TOTAL_WEEKS} weeks.")

        for week in weeks:
            if len(week.get("quiz_questions", [])) != config.QUIZ_QUESTIONS_PER_WEEK:
                raise ValueError(f"Week {week.get('week')} must have exactly 10 quiz questions.")

        return weeks

    def _load_next_week(self) -> None:
        self.week_index += 1
        if self.week_index >= len(self.weeks_data):
            self.state = "complete"
            self.dialogue = "Leon: You reached Knowledge Castle and rescued Course Mastery Score!"
            return

        self.level = Level(self.weeks_data[self.week_index])
        self.player.reset_position(*self.level.world.spawn_point)
        self.state = "gameplay"
        self.dialogue = self.leon.hint_for_mechanic(self.current_week_data["mechanic_type"])

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if self.state == "gameplay":
                    if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                        self.player.jump()
                elif self.state == "preboss":
                    if event.key == pygame.K_RETURN:
                        self.state = "quiz"
                        self.quiz_engine.start(self.current_week_data["quiz_questions"])
                        self.dialogue = self.armin.intro_line(
                            self.current_week_data["week"], self.current_week_data["topic"]
                        )
                elif self.state == "quiz":
                    key_map = {
                        pygame.K_a: "A",
                        pygame.K_b: "B",
                        pygame.K_c: "C",
                        pygame.K_d: "D",
                    }
                    if event.key in key_map:
                        self.quiz_engine.submit_answer(key_map[event.key])
                        if self.quiz_engine.finished:
                            result = self.quiz_engine.result()
                            if result.passed:
                                self.player.reward_xp(25)
                                self.quiz_message = self.armin.pass_line(result.score)
                                self.state = "week_result"
                            else:
                                self.quiz_message = self.armin.fail_line(result.score)
                                self.quiz_engine.start(self.current_week_data["quiz_questions"])
                elif self.state == "week_result" and event.key == pygame.K_RETURN:
                    self._load_next_week()

    def update_gameplay(self) -> None:
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(self.level.world.platforms)
        self.level.update()

        if self.player.rect.y > config.SCREEN_HEIGHT + 80:
            self.player.damage(6)
            self.player.reset_position(*self.level.world.spawn_point)

        for enemy in self.level.world.enemies:
            if enemy.alive and self.player.rect.colliderect(enemy.rect):
                damage, xp_reward = enemy.on_player_collision()
                self.player.damage(damage)
                self.player.reward_xp(xp_reward)

        if self.level.maybe_activate_boss(self.player.rect):
            self.dialogue = self.leon.pre_boss_line(self.current_week_data["topic"])

        if self.level.boss_active and self.level.boss.alive and self.player.rect.colliderect(self.level.boss.rect):
            if self.player.vel_y > 2 and self.player.rect.bottom <= self.level.boss.rect.centery + 16:
                defeated = self.level.boss.take_hit(7)
                self.player.vel_y = config.JUMP_FORCE * 0.5
                if defeated:
                    self.player.reward_xp(18)
                    self.state = "preboss"
                    self.dialogue = "Leon: Great win. Press Enter to face Armin's quiz gate."
            else:
                self.player.damage(5)

        if self.player.stats.hp <= 0:
            self.player.stats.hp = config.PLAYER_MAX_HP
            self.player.stats.stamina = config.PLAYER_MAX_STAMINA
            self.player.reset_position(*self.level.world.spawn_point)
            self.dialogue = "Leon: Reset done. Keep going—you can still pass this week."

    def update(self) -> None:
        if self.state == "gameplay":
            self.update_gameplay()

    def render(self) -> None:
        bg = config.WEEK_BG_COLORS[(self.current_week_data["week"] - 1) % len(config.WEEK_BG_COLORS)]
        self.screen.fill(bg)

        camera_x = max(0, min(self.player.rect.centerx - config.SCREEN_WIDTH // 2, 450))
        self.level.draw(self.screen, camera_x, config.COLORS)

        pygame.draw.rect(
            self.screen,
            config.COLORS["player"],
            pygame.Rect(self.player.rect.x - camera_x, self.player.rect.y, self.player.rect.width, self.player.rect.height),
            border_radius=6,
        )

        self.ui.draw_hud(
            self.screen,
            self.current_week_data["week"],
            self.current_week_data["topic"],
            self.player.stats.xp,
            self.player.stats.stamina,
            self.player.stats.hp,
        )
        self.ui.draw_objectives(self.screen, self.current_week_data["objectives"])

        if self.state == "quiz":
            question = self.quiz_engine.current_question()
            if question is not None:
                self.ui.draw_quiz_overlay(self.screen, question, self.quiz_engine.index + 1)

        if self.state == "week_result":
            self.ui.draw_dialogue(self.screen, f"{self.quiz_message} Press Enter for next week.")
        elif self.state == "complete":
            self.ui.draw_dialogue(self.screen, "Armin: Final clearance approved. Course mastery achieved!")
        else:
            self.ui.draw_dialogue(self.screen, self.dialogue)

        pygame.display.flip()

    async def tick(self) -> None:
        self.clock.tick(config.FPS)
        self.process_events()
        self.update()
        self.render()
