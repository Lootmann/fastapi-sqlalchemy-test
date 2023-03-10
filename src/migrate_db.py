from sqlalchemy import create_engine

from src.db import DATABASE_URL
from src.models.comment import Base as comment_base
from src.models.post import Base as post_base
from src.models.user import Base as user_base

engine = create_engine(DATABASE_URL, echo=True)


def reset_database():
    user_base.metadata.drop_all(bind=engine)
    user_base.metadata.create_all(bind=engine)

    post_base.metadata.drop_all(bind=engine)
    post_base.metadata.create_all(bind=engine)

    comment_base.metadata.drop_all(bind=engine)
    comment_base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
