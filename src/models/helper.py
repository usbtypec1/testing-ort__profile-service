from pydantic import BaseModel


class GenderOut(BaseModel):
    name: str
    value: int
