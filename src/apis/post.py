from typing import List

from sqlalchemy.orm import Session

from src.models import comment as comment_model
from src.models import post as post_model
from src.models import user as user_model
from src.schemas import post as post_schema


def get_all_posts(db: Session) -> List[post_schema.Post]:
    return db.query(post_model.Post).all()


def find_post_by_id(db: Session, post_id: int) -> post_schema.Post:
    return db.get(post_model.Post, post_id)


def create_post(
    db: Session, user: user_model.User, post_body: post_schema.PostCreate
) -> post_model.Post:
    post: post_model.Post = post_model.Post(**post_body.dict())
    user.posts.append(post)

    db.add(user)
    db.commit()
    db.refresh(user)

    return post


def update_post(
    db: Session, updated: post_model.Post, post_body: post_schema.PostCreate
) -> post_model.Post:
    updated.title = post_body.title
    updated.content = post_body.content

    db.add(updated)
    db.commit()
    db.refresh(updated)

    return updated


def delete_post(db: Session, post: post_model.Post) -> None:
    db.delete(post)
    db.commit()
    return
