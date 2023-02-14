from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import get_db
from src.schemas import user as user_schema
from src.schemas import post as post_schema
from src.apis import user as user_api
from src.apis import post as post_api

router = APIRouter()


@router.get("/posts")
def get_all_posts():
    return {"status": "posts"}


@router.get("/posts/{post_id}", response_model=post_schema.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = post_api.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found",
        )

    return post
