from pydantic import BaseModel, Field


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

    class Config:
        orm_mode = True
