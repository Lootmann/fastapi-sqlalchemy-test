from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]

    # ForeignKey
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post (id, title, content, user_id) = {self.id},{self.title},{self.content},{self.user_id})>"
