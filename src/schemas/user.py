from typing import List
from pydantic import BaseModel, Field

from src.schemas.post import Post
from src.schemas.comment import Comment


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    posts: List[Post] = Field([])
    comments: List[Comment] = Field([])

    class Config:
        orm_mode = True
