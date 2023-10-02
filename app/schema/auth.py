from typing import TypeVar, Union

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    full_name: str
    email: str
    avatar_url: Union[str, None] = None
    password: str


class RolePermissionSchema(BaseModel):
    permission = str