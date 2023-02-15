from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class CommentCreateResponse(CommentBase):
    user_id: int
    post_id: int


class Comment(CommentBase):
    user_id: int
    post_id: int
