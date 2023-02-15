from typing import List

from pydantic import BaseModel, Field

from src.schemas.comment import Comment
from src.schemas.post import Post


class UserBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserBase):
    id: int


class User(UserBase):
    id: int
    posts: List[Post] = Field([])
    comments: List[Comment] = Field([])
