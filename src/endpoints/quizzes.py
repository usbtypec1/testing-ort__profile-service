from fastapi import APIRouter, Depends

import models
from endpoints.depends import get_quiz_repository, get_current_user
from repositories.quizzes import QuizRepository

router = APIRouter()


@router.get('/{pk}', response_model=models.QuizJSON)
async def get_quiz_by_id(pk: int, current_user: models.User = Depends(get_current_user),
                         quizzes: QuizRepository = Depends(get_quiz_repository)):
    return await quizzes.get_by_id(pk)


@router.get('/', response_model=list[models.QuizPreview])
async def get_quizzes_list(
        limit: int = 100, skip: int = 0,
        current_user: models.User = Depends(get_current_user),
        quizzes: QuizRepository = Depends(get_quiz_repository),
):
    return await quizzes.get_all(limit, skip)


@router.post('/', response_model=models.QuizJSON)
async def create_quiz(
        quiz_json: models.QuizJSON,
        current_user: models.User = Depends(get_current_user),
        quizzes: QuizRepository = Depends(get_quiz_repository),
):
    return await quizzes.create(quiz_json, current_user)
