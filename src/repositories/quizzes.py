import json
import uuid

from sqlalchemy import insert, select

import db
import models
from core import config
from repositories.base import BaseRepository


class QuizRepository(BaseRepository):

    async def get_by_id(self, pk: int) -> models.QuizJSON:
        query = select(db.Quiz).where(db.Quiz.id == pk)
        quiz = await self._database.fetch_one(query)
        with open(quiz.quiz_file_path, encoding='utf-8') as file:
            quiz_file = json.load(file)
        quiz_model = models.QuizJSON.parse_obj(quiz_file)
        quiz_model.id = pk
        return quiz_model

    async def get_all(self, limit: int, skip: int = 0) -> list[models.QuizPreview]:
        query = select(db.Quiz).order_by(db.Quiz.created_at.desc()).limit(limit).offset(skip)
        quizzes = await self._database.fetch_all(query)
        return [models.QuizPreview(
            id=quiz.id,
            name=quiz.name,
            description=quiz.description,
            thumbnail_url=quiz.thumbnail_url,
            created_at=quiz.created_at,
        ) for quiz in quizzes]

    async def create(self, quiz_json: models.QuizJSON, user: models.User) -> models.QuizJSON:
        file_path = config.QUIZZES_DIR / f'{uuid.uuid4().hex}.json'
        query = insert(db.Quiz).values(quiz_file_path=str(file_path),
                                       thumbnail_url=quiz_json.thumbnail_url,
                                       name=quiz_json.name,
                                       description=quiz_json.description,
                                       created_by_user=user.id)
        quiz_id = await self._database.execute(query)
        with open(file_path, 'w', encoding='utf-8') as file:
            json_dict = quiz_json.dict()
            json_dict['id'] = quiz_id
            json.dump(json_dict, file, ensure_ascii=False)
        quiz_json.id = quiz_id
        return quiz_json
