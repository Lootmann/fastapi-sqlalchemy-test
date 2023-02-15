from typing import List
from sqlalchemy.orm import Session
from src.schemas import comment as comment_schema
from src.models import post as post_model, comment as comment_model


def get_all_comments(db: Session) -> List[comment_model.Comment]:
    return db.query(comment_model.Comment).all()


def find_comment_by_id(db: Session, comment_id: int) -> comment_model.Comment | None:
    return db.get(comment_model.Comment, comment_id)


def create_comment(
    db: Session, post: post_model.Post, comment_body: comment_schema.CommentCreate
) -> comment_model.Comment:
    comment: comment_model.Comment = comment_model.Comment(**comment_body.dict())
    post.comments.append(comment)

    db.add(post)
    db.commit()
    db.refresh(post)

    return comment


def update_comment(
    db: Session, updated: comment_model.Comment, comment_body: comment_schema.CommentCreate
) -> comment_model.Comment:
    updated.comment = comment_body.comment

    db.add(updated)
    db.commit()
    db.refresh(updated)

    return updated


def delete_comment(db: Session, comment: comment_model.Comment) -> None:
    db.delete(comment)
    db.commit()
    return
