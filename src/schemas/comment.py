from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    user_id: int
    post_id: int


class CommentCreateResponse(CommentBase):
    id: int
    user_id: int
    post_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int


"""
class PostBase(BaseModel):
    title: str = Field("")
    content: str = Field("")

class PostCreate(PostBase):
    user_id: int

class PostCreateResponse(PostBase):
    id: int

class Post(PostBase):
    id: int
    user_id: int
    comments: List[Comment]
"""
