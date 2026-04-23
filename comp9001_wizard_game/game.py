"""Main gameplay loop and progression logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import pygame

import config
from events import get_random_event
from ui import UIManager


@dataclass
class WeekContent:
    week: int
    title: str
    topic: str
    scenario: str
    choices: Dict[str, Dict[str, object]]
    color: tuple[int, int, int]


class Game:
    """Story-driven RPG simulation for COMP9001-style learning progression."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.ui = UIManager(screen)
        self.player = config.PLAYER_PROFILE
        self.current_week = 1
        self.stats = config.get_starting_stats(self.player["background"])
        self.running = True
        self.weeks = self._build_weeks()

    def _build_weeks(self) -> List[WeekContent]:
        """Define week content in data so future weeks are easy to add."""
        return [
            WeekContent(
                week=1,
                title="Week 1",
                topic="Introduction to Programming / First Program",
                scenario="Your lecturer asks everyone to build a first Python script before tutorial.",
                choices={
                    "1": {
                        "label": "Study after class",
                        "effects": {"xp": 16, "time": -12},
                        "result": "You practised syntax and gained confidence.",
                    },
                    "2": {
                        "label": "Skip and hope to catch up",
                        "effects": {"xp": -6, "time": 8},
                        "result": "You saved time now, but missed core foundations.",
                    },
                    "3": {
                        "label": "Seek help from guide",
                        "effects": {"xp": 12, "time": -9},
                        "result": "The guide helped you create your first program step by step.",
                    },
                },
                color=(30, 45, 90),
            ),
            WeekContent(
                week=2,
                title="Week 2",
                topic="Programming Basics / Variables & Data Types",
                scenario="A quiz covers variables, casting, and common type mistakes.",
                choices={
                    "1": {
                        "label": "Revise and complete extra exercises",
                        "effects": {"xp": 18, "time": -14},
                        "result": "Your variable handling became much stronger.",
                    },
                    "2": {
                        "label": "Do minimum tasks only",
                        "effects": {"xp": 4, "time": -5},
                        "result": "You progressed, but only at a shallow level.",
                    },
                    "3": {
                        "label": "Attend mentor clinic",
                        "effects": {"xp": 14, "time": -10},
                        "result": "The mentor clarified data types with practical examples.",
                    },
                },
                color=(45, 90, 60),
            ),
            WeekContent(
                week=3,
                title="Week 3",
                topic="Variables Reinforcement / Conditionals",
                scenario="You must write logic with if/elif/else under time pressure.",
                choices={
                    "1": {
                        "label": "Build a mini challenge project",
                        "effects": {"xp": 22, "time": -16},
                        "result": "You mastered conditionals through applied practice.",
                    },
                    "2": {
                        "label": "Focus on surviving deadline",
                        "effects": {"xp": 7, "time": -7},
                        "result": "You passed tasks, but conceptual gaps remain.",
                    },
                    "3": {
                        "label": "Ask both mentor and guide",
                        "effects": {"xp": 17, "time": -13},
                        "result": "Support helped you turn confusion into clear logic.",
                    },
                },
                color=(95, 50, 90),
            ),
        ]

    def _stats_text(self) -> str:
        return (
            f"Student: {self.player['name']} | Course: {self.player['course']} | "
            f"Week: {self.current_week}/3 | XP: {self.stats['xp']} | Time: {self.stats['time']}"
        )

    def _apply_effects(self, effects: Dict[str, int]) -> None:
        for stat_name, value in effects.items():
            self.stats[stat_name] += value
        self.stats["xp"] = max(0, self.stats["xp"])
        self.stats["time"] = max(0, self.stats["time"])

    def _mentor_dialogue(self) -> str:
        background = self.player["background"]
        if background == "wealthy":
            return "Mentor: Resources help, but consistency still decides outcomes."
        if background == "middle":
            return "Mentor: Balance your effort wisely—consistency beats short bursts."
        return "Mentor: Your path is harder; ask for help early and protect your energy."

    def _guide_dialogue(self) -> str:
        background = self.player["background"]
        if background == "wealthy":
            return "Guide Leon: I can connect you to premium support, but it costs time."
        if background == "middle":
            return "Guide Leon: I can help review your code if you can spare study time."
        return "Guide Leon: I can help for free, but you'll need patience and steady practice."

    def _ending_text(self) -> str:
        xp = self.stats["xp"]
        time_left = self.stats["time"]

        if xp >= 125:
            return "Ending: Top Performer — You finished as one of the strongest students."
        if xp >= 95:
            return "Ending: Passed Successfully — Solid result with steady progress."
        if xp >= 80 and time_left <= 25:
            return "Ending: Late Comeback — You struggled early but recovered in the final week."
        if xp < 80 and time_left < 22:
            return "Ending: Struggled / Burnout — Inequality pressures drained your momentum."
        return "Ending: Survived the Course — You completed the term with valuable lessons."

    def _apply_background_catchup(self, week_number: int) -> Optional[str]:
        """Give lower-income players a late support path without removing challenge."""
        if self.player["background"] == "lower" and week_number >= 2 and self.stats["xp"] < 95:
            self._apply_effects({"xp": 6, "time": -2})
            return "Support grant: Community tutoring gave you +6 XP for persistence."
        return None

    async def _collect_player_setup(self) -> bool:
        """Collect player personalization inside pygame for pygbag compatibility."""
        name = await self.ui.prompt_text(
            title="Student Setup",
            prompt="Enter your name:",
            helper_text="Press Enter to confirm.",
            default_text="Student",
        )
        if name is None:
            return False

        course = await self.ui.prompt_text(
            title="Course Setup",
            prompt="Enter course name:",
            helper_text="Press Enter to confirm (default COMP9001).",
            default_text="COMP9001",
        )
        if course is None:
            return False

        choices = {"1": "Wealthy", "2": "Middle-income", "3": "Lower-income"}
        self.ui.draw_scene(
            title="Background Selection",
            lines=[
                "Choose your socioeconomic background.",
                "This affects your starting XP/time and event pressures.",
            ],
            choices=choices,
            stats_text="Select 1, 2, or 3.",
            background_color=(20, 30, 60),
        )
        selected = await self.ui.wait_for_choice(choices.keys())
        if selected is None:
            return False

        background = config.BACKGROUND_LABELS[selected]
        config.set_player_profile(name=name, course=course, background=background)
        self.player = config.PLAYER_PROFILE
        self.stats = config.get_starting_stats(background)
        self.current_week = 1
        return True

    async def run(self) -> None:
        if not await self._collect_player_setup():
            return

        intro_choices = {"1": "Begin your semester adventure"}
        self.ui.draw_scene(
            title="Welcome to the Wizard of COMP9001",
            lines=[
                f"{self.player['name']}, you are entering {self.player['course']}.",
                f"Background: {config.BACKGROUND_NAMES[self.player['background']]}",
                "Over 3 weeks, your choices, support network, and resources shape your outcomes.",
            ],
            choices=intro_choices,
            stats_text=self._stats_text(),
            background_color=(25, 25, 45),
        )
        if await self.ui.wait_for_choice(intro_choices.keys()) is None:
            return

        for week in self.weeks:
            event = get_random_event(self.player["background"])
            self._apply_effects(event["effects"])

            catchup_note = self._apply_background_catchup(week.week)

            lines = [
                f"Topic: {week.topic}",
                week.scenario,
                f"Random event: {event['name']} — {event['description']}",
                self._mentor_dialogue(),
                self._guide_dialogue(),
            ]
            if catchup_note:
                lines.append(catchup_note)

            choice_map = {key: item["label"] for key, item in week.choices.items()}
            self.ui.draw_scene(
                title=week.title,
                lines=lines,
                choices=choice_map,
                stats_text=self._stats_text(),
                background_color=week.color,
            )

            selected = await self.ui.wait_for_choice(choice_map.keys())
            if selected is None:
                self.running = False
                break

            chosen = week.choices[selected]
            self._apply_effects(chosen["effects"])

            outcome_choices = {"1": "Continue"}
            self.ui.draw_scene(
                title=f"Week {week.week} Outcome",
                lines=[
                    str(chosen["result"]),
                    f"XP change: {chosen['effects']['xp']} | Time change: {chosen['effects']['time']}",
                    f"Current totals → XP: {self.stats['xp']} | Time: {self.stats['time']}",
                ],
                choices=outcome_choices,
                stats_text=self._stats_text(),
                background_color=week.color,
            )
            if await self.ui.wait_for_choice(outcome_choices.keys()) is None:
                self.running = False
                break

            self.current_week += 1

        final_choices = {"1": "Exit game"}
        self.ui.draw_scene(
            title="Semester Complete",
            lines=[
                self._ending_text(),
                "Thank you for playing this inequality-aware learning simulation.",
                "Tip: replay with another background and compare outcomes.",
            ],
            choices=final_choices,
            stats_text=self._stats_text(),
            background_color=(20, 20, 20),
        )
        await self.ui.wait_for_choice(final_choices.keys())
