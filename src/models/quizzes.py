from datetime import datetime

from pydantic import BaseModel


class QuizPreview(BaseModel):
    id: int
    name: str
    description: str
    thumbnail_url: str
    created_at: datetime


class QuizAnswer(BaseModel):
    answer: str
    is_correct: bool


class QuizQuestion(BaseModel):
    question: str
    answers: list[QuizAnswer]


class QuizJSON(BaseModel):
    id: int | None = None
    name: str
    description: str
    thumbnail_url: str
    quiz: list[QuizQuestion]
