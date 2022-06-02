from datetime import datetime

from pydantic import BaseModel


class QuizPreview(BaseModel):
    id: int
    name: str
    description: str
    thumbnail_url: str
    created_at: datetime


class QuizQuestion(BaseModel):
    question: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    correct_answer: str


class QuizJSON(BaseModel):
    id: int | None = None
    name: str
    description: str
    thumbnail_url: str
    quiz: list[QuizQuestion]
