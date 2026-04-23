"""Quiz system that gates week progression after each boss."""

from __future__ import annotations

from dataclasses import dataclass

import config


@dataclass
class QuizResult:
    passed: bool
    score: int


class QuizEngine:
    def __init__(self) -> None:
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

    def submit_answer(self, option: str) -> None:
        question = self.current_question()
        if question is None:
            return

        if option.upper() == str(question["answer"]).upper():
            self.score += 1

        self.index += 1
        if self.index >= len(self.questions):
            self.finished = True

    def result(self) -> QuizResult:
        return QuizResult(passed=self.score >= config.QUIZ_PASS_SCORE, score=self.score)
