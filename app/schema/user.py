from pydantic import BaseModel


class UserValidate(BaseModel):
    page: int
    page_size: int
    search: str
