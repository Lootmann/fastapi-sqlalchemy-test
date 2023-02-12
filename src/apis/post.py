from typing import List
from sqlalchemy.orm import Session
from src.schemas import post as post_schema
from src.models import post as post_model


def get_all_posts_by_user(db: Session, user_id: int) -> List[post_schema.Post]:
    return (
        db.query(post_model.Post)
        .where(post_model.Post.user_id == user_id)
        .all()
    )


def get_post_by_post_id(db: Session, post_id: int) -> post_schema.Post:
    return (
        db.query(post_model.Post).where(post_model.Post.id == post_id).first()
    )


def create_post(
    db: Session, user_id: int, post_body: post_schema.PostCreate
) -> post_model.Post:
    data = {}
    data.update(**post_body.dict())
    data.update({"user_id": user_id})
    post = post_model.Post(**data)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post
