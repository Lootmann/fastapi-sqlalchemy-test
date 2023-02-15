from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.apis import post as post_api
from src.apis import user as user_api
from src.schemas import post as post_schema
from src.db import get_db

router = APIRouter()


@router.get("/posts", response_model=List[post_schema.Post])
def get_all_posts(db: Session = Depends(get_db)):
    return post_api.get_all_posts(db)


@router.get("/posts/{post_id}", response_model=post_schema.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = post_api.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post:{post_id} Not Found")
    return post


@router.get("/posts/{post_id}/comments")
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return {}


@router.get("/posts/{post_id}/comments/{comment_id}")
def get_comment_by_post(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    return {}


@router.post("/posts", response_model=post_schema.PostCreateResponse, status_code=201)
def create_post(post_body: post_schema.PostCreate, db: Session = Depends(get_db)):
    user = user_api.find_user_by_id(db, post_body.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User:{post_body.user_id} Not Found")
    return post_api.create_post(db, user, post_body)


@router.put("/posts/{post_id}")
def update_post(post_id: int, db: Session = Depends(get_db)):
    return {}


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return {}
