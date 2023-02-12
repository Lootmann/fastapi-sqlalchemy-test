from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import get_db
from src.schemas import user as user_schema
from src.schemas import post as post_schema
from src.apis import user as user_api
from src.apis import post as post_api

router = APIRouter()


@router.get("/status")
def server_status():
    return {"status": "seems fine :^)"}


@router.get("/users", response_model=List[user_schema.User])
def get_all_users(db: Session = Depends(get_db)):
    return user_api.get_all_users(db)


@router.get("/users/{user_id}", response_model=user_schema.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    result = user_api.get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return result


@router.post("/users", response_model=user_schema.UserCreateResponse)
def create_user(
    user_body: user_schema.UserCreate, db: Session = Depends(get_db)
):
    return user_api.create_user(db, user_body)


@router.get("/users/{user_id}/posts", response_model=List[post_schema.Post])
def get_all_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    result = user_api.get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return post_api.get_all_posts_by_user(db, user_id)


@router.get("/users/{user_id}/posts/{post_id}", response_model=post_schema.Post)
def get_post_by_user(user_id: int, post_id: int, db: Session = Depends(get_db)):
    result = user_api.get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )

    post = post_api.get_post_by_post_id(db, post_id)
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )

    return post


@router.post("/users/{user_id}/posts")
def create_post(
    user_id: int,
    post_body: post_schema.PostCreate,
    db: Session = Depends(get_db),
):
    result = user_api.get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return post_api.create_post(db, user_id, post_body)
