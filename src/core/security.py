from datetime import datetime, timedelta

import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext

from core import config

pwd_context = CryptContext(schemes=['bcrypt'])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()
    to_encode['exp'] = datetime.utcnow() + timedelta(days=1)
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        return credentials.credentials
