from enum import IntEnum

from pydantic import BaseModel, EmailStr, constr

__all__ = (
    'UserIn',
    'User',
    'UserToUpdate',
    'UserOut',
    'Gender',
)


class Gender(IntEnum):
    MALE = 0
    FEMALE = 1
    OTHER = 2


class User(BaseModel):
    id: int | None
    email: EmailStr
    hashed_password: str
    first_name: str | None
    last_name: str | None
    gender: str | None


class UserToUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    gender: Gender | None


class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: constr(max_length=64) | None
    last_name: constr(max_length=64) | None
    gender: Gender | None
