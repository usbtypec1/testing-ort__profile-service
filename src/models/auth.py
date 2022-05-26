from pydantic import BaseModel, constr, EmailStr


class AccessCredentials(BaseModel):
    access_string: str
    token_type: str


class AuthCredentials(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
