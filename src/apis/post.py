from typing import List
from sqlalchemy.orm import Session
from src.schemas import post as post_schema
from src.models import post as post_model
from src.models import user as user_model


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
    user: user_model.User = (
        db.query(user_model.User).filter(user_model.User.id == user_id).first()
    )

    post: post_model.Post = post_model.Post(**post_body.dict())

    user.posts.append(post)
    db.add(user)
    db.commit()
    db.refresh(user)

    return post
