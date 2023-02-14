from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str


class Comment(CommentBase):
    user_id: int
    post_id: int
