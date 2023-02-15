from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.db import Base


class Comment(Base):
    """
    Post : Comment = 1 : n = A Post has Many Comments
    so, `posts` relation which has backref, not backpopulates might be OK
    """

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Comment (id,comment,user_id,post_id) = ({self.id},{self.comment},{self.user_id},{self.post_id})>"
