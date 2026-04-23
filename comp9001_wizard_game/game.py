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


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.ui = UI()

        self.weeks = self._load_weeks()
        self.week_idx = 0

        self.player = Player(80, 400)
        self.level = Level(self.week_data)
        self.quiz = QuizEngine()

        self.leon = MentorNPC()
        self.armin = ArminGatekeeper()

        self.state = "gameplay"
        self.dialogue = self.leon.mechanic_hint(self.week_data["mechanic_type"])
        self.quiz_feedback = ""
        self.running = True

    @property
    def week_data(self) -> dict:
        return self.weeks[self.week_idx]

    def _load_weeks(self) -> list[dict]:
        path = Path(__file__).resolve().parent / "data" / "weeks.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if len(data) < config.TOTAL_WEEKS:
            raise ValueError("weeks.json must contain 13 weeks")
        for item in data:
            if len(item.get("quiz_questions", [])) != config.QUIZ_QUESTIONS_PER_WEEK:
                raise ValueError(f"Week {item.get('week')} must have 10 quiz questions")
        return data

    def _next_week(self) -> None:
        self.week_idx += 1
        if self.week_idx >= len(self.weeks):
            self.state = "complete"
            self.dialogue = "Leon: You rescued the Course Mastery Score from Knowledge Castle!"
            return
        self.level = Level(self.week_data)
        self.player.reset_position(*self.level.world.spawn)
        self.state = "gameplay"
        self.dialogue = self.leon.mechanic_hint(self.week_data["mechanic_type"])

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if self.state == "gameplay" and event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                    self.player.jump()
                elif self.state == "preboss" and event.key == pygame.K_RETURN:
                    self.state = "quiz"
                    self.quiz.start(self.week_data["quiz_questions"])
                    self.dialogue = self.armin.intro(self.week_data["week"], self.week_data["topic"])
                elif self.state == "quiz":
                    key_to_answer = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D"}
                    if event.key in key_to_answer:
                        self.quiz.submit(key_to_answer[event.key])
                        if self.quiz.finished:
                            result = self.quiz.result()
                            if result.passed:
                                self.player.reward_xp(25)
                                self.quiz_feedback = self.armin.passed(result.score)
                                self.state = "week_result"
                            else:
                                self.quiz_feedback = self.armin.failed(result.score)
                                self.quiz.start(self.week_data["quiz_questions"])
                elif self.state == "week_result" and event.key == pygame.K_RETURN:
                    self._next_week()

    def _update_gameplay(self) -> None:
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(self.level.world.platforms)
        self.level.update()

        if self.player.rect.y > config.SCREEN_HEIGHT + 80:
            self.player.damage(6)
            self.player.reset_position(*self.level.world.spawn)

        for enemy in self.level.world.enemies:
            if enemy.alive and self.player.rect.colliderect(enemy.rect):
                dmg, xp = enemy.collide_player()
                self.player.damage(dmg)
                self.player.reward_xp(xp)

        if self.level.maybe_activate_boss(self.player.rect):
            self.dialogue = self.leon.pre_boss(self.week_data["topic"])

        if self.level.boss_active and self.level.boss.alive and self.player.rect.colliderect(self.level.boss.rect):
            if self.player.vel_y > 2 and self.player.rect.bottom <= self.level.boss.rect.centery + 16:
                defeated = self.level.boss.take_hit(7)
                self.player.vel_y = config.JUMP_FORCE * 0.5
                if defeated:
                    self.player.reward_xp(18)
                    self.state = "preboss"
                    self.dialogue = "Leon: Boss defeated. Press Enter for Armin's quiz gate."
            else:
                self.player.damage(5)

        if self.player.stats.hp <= 0:
            self.player.stats.hp = config.PLAYER_MAX_HP
            self.player.stats.stamina = config.PLAYER_MAX_STAMINA
            self.player.reset_position(*self.level.world.spawn)
            self.dialogue = "Leon: You reset at checkpoint. Keep going."

    def _render(self) -> None:
        bg = config.WEEK_BG_COLORS[(self.week_data["week"] - 1) % len(config.WEEK_BG_COLORS)]
        self.screen.fill(bg)

        camera_x = max(0, min(self.player.rect.centerx - config.SCREEN_WIDTH // 2, 450))
        self.level.draw(self.screen, camera_x, config.COLORS)

        pygame.draw.rect(
            self.screen,
            config.COLORS["player"],
            pygame.Rect(self.player.rect.x - camera_x, self.player.rect.y, self.player.rect.width, self.player.rect.height),
            border_radius=6,
        )

        self.ui.draw_hud(self.screen, self.week_data["week"], self.week_data["topic"], self.player.stats.xp, self.player.stats.stamina, self.player.stats.hp)
        self.ui.draw_objectives(self.screen, self.week_data.get("objectives", self.week_data.get("learning_objectives", [])))

        if self.state == "quiz":
            q = self.quiz.current_question()
            if q:
                self.ui.draw_quiz(self.screen, q, self.quiz.index + 1)

        if self.state == "week_result":
            self.ui.draw_dialogue(self.screen, f"{self.quiz_feedback} Press Enter for next week.")
        elif self.state == "complete":
            self.ui.draw_dialogue(self.screen, "Armin: Final clearance approved. COMP9001 mastery achieved.")
        else:
            self.ui.draw_dialogue(self.screen, self.dialogue)

        pygame.display.flip()

    async def tick(self) -> None:
        self.clock.tick(config.FPS)
        self._handle_events()
        if self.state == "gameplay":
            self._update_gameplay()
        self._render()
