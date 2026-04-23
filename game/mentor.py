"""Mentor and professor dialogue systems."""

from __future__ import annotations

import config


class MentorNPC:
    name = "Leon"

    def hint_for_mechanic(self, mechanic_type: str) -> str:
        theme = config.MECHANIC_THEME.get(mechanic_type, "adapt and learn")
        return f"Leon: Focus on {theme}. Observe patterns before rushing."

    def pre_boss_line(self, topic: str) -> str:
        return f"Leon: Boss ahead. Use what you learned about {topic.lower()} and stay calm."


class ArminGatekeeper:
    name = "Armin"

    def intro_line(self, week_number: int, topic: str) -> str:
        return f"Armin: Week {week_number} complete? Prove mastery in {topic}. 10 questions."

    def pass_line(self, score: int) -> str:
        return f"Armin: Acceptable. {score}/10. You may progress."

    def fail_line(self, score: int) -> str:
        return f"Armin: {score}/10 is insufficient. Retry the quiz gate immediately."
