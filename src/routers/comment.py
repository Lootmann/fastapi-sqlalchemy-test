from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlalchemy.orm import Session

from src.schemas import comment as comment_schema
from src.apis import post as post_api
from src.apis import comment as comment_api
from src.db import get_db


router = APIRouter()


@router.get("/comments", response_model=List[comment_schema.Comment])
def get_all_comments(db: Session = Depends(get_db)):
    return comment_api.get_all_comments(db)


@router.get("/comments/{comment_id}", response_model=comment_schema.Comment)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_api.find_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment:{comment_id} Not Found")
    return comment


@router.post(
    "/comments",
    response_model=comment_schema.CommentCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(comment_body: comment_schema.CommentCreate, db: Session = Depends(get_db)):
    # TODO: get current user
    post = post_api.find_post_by_id(db, comment_body.post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post:{comment_body.post_id} Not Found")
    return comment_api.create_comment(db, post, comment_body)


@router.delete(
    "/comments/{comment_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    # TODO: get current user, and check current_user.id == comment.user_id
    comment = comment_api.find_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail=f"Comment:{comment_id} Not Found")
    return comment_api.delete_comment(db, comment)
