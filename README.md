# FastAPI + SQLAlchemy

Relation のテスト

## Model

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[List["Post"]] = relationship("Post", backref="user")

    def __repr__(self) -> str:
        return f"<User (id, name, posts) {self.id},{self.name},{self.posts}>"
```

```python
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Post (id, title, content, user_id) = {self.id},{self.title},{self.content},{self.user_id})>"
```
