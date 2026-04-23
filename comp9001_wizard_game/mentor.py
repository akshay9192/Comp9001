from __future__ import annotations

import config


class MentorNPC:
    name = "Leon"

    def mechanic_hint(self, mechanic: str) -> str:
        return f"Leon: {config.MECHANIC_HINTS.get(mechanic, 'Learn, adapt, and stay calm.')}"

    def pre_boss(self, topic: str) -> str:
        return f"Leon: Boss ahead. Apply {topic.lower()} carefully and keep your rhythm."


class ArminGatekeeper:
    name = "Armin"

    def intro(self, week: int, topic: str) -> str:
        return f"Armin: Week {week} clear? Show me mastery of {topic}. 10 questions now."

    def passed(self, score: int) -> str:
        return f"Armin: {score}/10. Acceptable. Next week unlocked."

    def failed(self, score: int) -> str:
        return f"Armin: {score}/10. Insufficient. Retry the quiz gate." 
