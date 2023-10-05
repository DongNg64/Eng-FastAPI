from typing import Union

from pydantic import BaseModel


class UserValidate(BaseModel):
    page: int
    page_size: int
    search: Union[str, None] = None


class UserSchema(BaseModel):
    id: str
    full_name: str
    email: str
    # phone: str
    type: str
