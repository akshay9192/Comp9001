from __future__ import annotations

from dataclasses import dataclass

import config


@dataclass
class QuizResult:
    passed: bool
    score: int


class QuizEngine:
    def __init__(self):
        self.questions: list[dict] = []
        self.index = 0
        self.score = 0
        self.finished = False

    def start(self, questions: list[dict]) -> None:
        self.questions = questions[: config.QUIZ_QUESTIONS_PER_WEEK]
        self.index = 0
        self.score = 0
        self.finished = False

    def current_question(self) -> dict | None:
        if self.finished or self.index >= len(self.questions):
            return None
        return self.questions[self.index]

    def submit(self, answer: str) -> None:
        q = self.current_question()
        if q is None:
            return
        if answer.upper() == str(q["answer"]).upper():
            self.score += 1
        self.index += 1
        if self.index >= len(self.questions):
            self.finished = True

    def result(self) -> QuizResult:
        return QuizResult(self.score >= config.QUIZ_PASS_SCORE, self.score)
