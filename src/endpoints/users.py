from fastapi import APIRouter, Depends, HTTPException, status

import models
from endpoints.depends import get_user_repository, get_current_user
from repositories.users import UserRepository

router = APIRouter()


@router.get('/me', response_model=models.UserOut)
async def get_me(current_user: models.User = Depends(get_current_user)):
    return models.UserOut.parse_obj(current_user.dict())


@router.post('/', response_model=models.UserOut)
async def create_user(
        user_in: models.UserIn,
        users: UserRepository = Depends(get_user_repository),
):
    return await users.create(user_in)


@router.get('/{pk}', response_model=models.UserOut)
async def get_user_by_pk(
        pk: int,
        users: UserRepository = Depends(get_user_repository)):
    return await users.get_by_id(pk, exclude_password=True)


@router.patch('/', response_model=models.UserToUpdate)
async def update_user(
        user_to_update: models.UserToUpdate,
        current_user: models.User = Depends(get_current_user),
        users: UserRepository = Depends(get_user_repository),
):
    return await users.update(current_user.id, user_to_update)
