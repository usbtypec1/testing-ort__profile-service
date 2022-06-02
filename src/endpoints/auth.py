from fastapi import APIRouter, Depends, Response

import models
from core import security, exceptions
from endpoints.depends import get_user_repository
from repositories.users import UserRepository

router = APIRouter()


@router.post('/', response_model=models.AccessCredentials)
async def auth(
        auth_credentials: models.AuthCredentials,
        users: UserRepository = Depends(get_user_repository),
):
    user = await users.get_by_email(auth_credentials.email)
    if not security.verify_password(auth_credentials.password, user.hashed_password):
        raise exceptions.UserDoesNotExist('Invalid password')
    token = security.create_access_token({'sub': user.id})
    return models.AccessCredentials(
        access_string=token,
        token_type='Bearer'
    )
