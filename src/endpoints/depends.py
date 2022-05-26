import jwt
from fastapi import Depends, HTTPException, status

import models
from core import security, exceptions
from repositories.users import UserRepository
from db.engine import database


def get_user_repository():
    return UserRepository(database)


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(security.JWTBearer()),
) -> models.User:
    try:
        payload = security.decode_access_token(token)
        user_id = payload['sub']
        user = await users.get_by_id(user_id)
    except (KeyError, jwt.DecodeError, exceptions.UserDoesNotExist):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Credentials are not valid')
    return user
