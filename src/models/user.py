from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")


from src.models.post import Post
