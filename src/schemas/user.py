from typing import List
from pydantic import BaseModel

from src.schemas.post import Post


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
    posts: List[Post] = []

    class Config:
        orm_mode = True
