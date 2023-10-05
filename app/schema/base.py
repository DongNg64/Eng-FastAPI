from typing import Generic, List, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel, EmailStr, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class RedisSaveSchema(BaseModel):
    id: str
    user_id: str
    # permissions: list(str)

# class RedisSchema(BaseModel):
#     permissions: json()


class EmailSchema(BaseModel):
    emails: List[EmailStr]