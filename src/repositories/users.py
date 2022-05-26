from asyncpg import UniqueViolationError
from sqlalchemy import insert, select, update

from repositories.base import BaseRepository
from core import security, exceptions
import models
import db


class UserRepository(BaseRepository):

    async def create(self, user_in: models.UserIn) -> models.UserOut:
        user = models.User(
            email=user_in.email,
            hashed_password=security.hash_password(user_in.password),
        )
        values = user.dict(exclude={'id'})
        query = insert(db.User).values(**values)
        values.pop('hashed_password')
        try:
            user_id = await self._database.execute(query)
        except UniqueViolationError:
            raise exceptions.UserEmailAlreadyUsed('User email already used')
        values['id'] = user_id
        return models.UserOut(**values)

    async def get_by_id(self, pk: int, exclude_password: bool = False) -> models.UserOut | models.User:
        query = select(db.User).where(db.User.id == pk)
        user = await self._database.fetch_one(query)
        if user is None:
            raise exceptions.UserDoesNotExist('User by provided ID is not found')
        if exclude_password:
            return models.UserOut.parse_obj(user)
        return models.User.parse_obj(user)

    async def get_by_email(self, email: str) -> models.User:
        query = select(db.User).where(db.User.email == email)
        user = await self._database.fetch_one(query)
        if user is None:
            raise exceptions.UserDoesNotExist('User by provided ID is not found')
        return models.User.parse_obj(user)

    async def update(self, pk: int, user_to_update: models.UserToUpdate) -> models.UserToUpdate:
        values = user_to_update.dict()
        query = update(db.User).values(**values).where(db.User.id == pk)
        await self._database.execute(query)
        return user_to_update
