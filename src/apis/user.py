from typing import List

from sqlalchemy.orm import Session

from src.models import comment as comment_model
from src.models import post as post_model
from src.models import user as user_model
from src.schemas import comment as comment_schema
from src.schemas import post as post_schema
from src.schemas import user as user_schema


def get_all_users(db: Session) -> List[user_model.User]:
    return db.query(user_model.User).all()


def create_user(db: Session, user_body: user_schema.UserCreate) -> user_model.User:
    user = user_model.User(**user_body.dict())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def find_user_by_id(db: Session, user_id: int) -> user_model.User | None:
    return db.get(user_model.User, user_id)


def find_posts_by_user_id(db: Session, user_id: int) -> List[post_model.Post]:
    # NOTE: db.get(User, user_id) response has posts[] field...
    return db.query(post_model.Post).filter(post_model.Post.user_id == user_id).all()


def find_post_by_user_id(db: Session, user_id: int, post_id) -> post_model.Post | None:
    return (
        db.query(post_model.Post)
        .filter(post_model.Post.user_id == user_id)
        .filter(post_model.Post.id == post_id)
        .first()
    )


def find_comments_by_user_id(db: Session, user_id: int) -> List[comment_model.Comment]:
    return db.query(comment_model.Comment).filter(comment_model.Comment.user_id == user_id).all()


def update_user(
    db: Session, updated: user_schema.User, user_body: user_schema.UserCreate
) -> user_model.User:
    user = user_model.User(**user_body.dict())
    updated.name = user.name

    db.add(updated)
    db.commit()
    db.refresh(updated)

    return updated


def delete_user(db: Session, user: user_model.User) -> None:
    db.delete(user)
    db.commit()
    return
