from typing import List
from pydantic import BaseModel, Field
from src.schemas.comment import Comment


class PostBase(BaseModel):
    title: str = Field("")
    content: str = Field("")


class PostCreate(PostBase):
    pass


class PostCreateResponse(PostCreate):
    id: int

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    user_id: int
    comments: List[Comment]

    class Config:
        orm_mode = True
