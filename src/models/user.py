from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from src.models.post import Post


class User(Base):
    """
    User : Post = 1 : n  - A User has Many posts
    so, `posts` relation which has backref, not backpopulates might be OK
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[List["Post"]] = relationship("Post", backref="user")

    def __repr__(self) -> str:
        return f"<User (id, name, posts) {self.id},{self.name},{self.posts}>"
