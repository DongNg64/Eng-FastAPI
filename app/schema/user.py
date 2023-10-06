from typing import Union, List

from pydantic import BaseModel

from app.schema.base import ResponseSchema


class UserValidate(BaseModel):
    page: int
    page_size: int
    search: Union[str, None] = None


class User(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str
    type: str


class UserSchema(ResponseSchema):
    pass
    # class Config:
    #     orm_mode = True
