from dataclasses import dataclass
from typing import Union, List

from pydantic import BaseModel

from app.schema.base import ResponseSchema


class UserValidate(BaseModel):
    full_name: str
    # phone: str


class UserSchema(BaseModel):
    id: Union[str, None] = None
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    type: Union[str, None] = None
    role_name: Union[str, None] = None

    class Config:
        orm_mode = True


class UsersSchema(ResponseSchema):
    result: Union[List[UserSchema], None] = None

