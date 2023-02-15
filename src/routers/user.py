from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.apis import user as user_api
from src.db import get_db
from src.schemas import user as user_schema
from src.schemas import post as post_schema

router = APIRouter()


@router.get("/users", response_model=List[user_schema.User])
def get_all_users(db: Session = Depends(get_db)):
    return user_api.get_all_users(db)


@router.post("/users", response_model=user_schema.UserCreateResponse)
def create_user(user_body: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_api.create_user(db, user_body)


@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse, status_code=201)
def update_user(user_id: int, user_body: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_api.find_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User:{user_id} Not Found")
    return user_api.update_user(db, user, user_body)


@router.delete("/users/{user_id}", response_model=None)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_api.find_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User:{user_id} Not Found")
    return user_api.delete_user(db, user)


@router.get("/users/{user_id}", response_model=user_schema.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_api.find_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User:{user_id} Not Found")
    return user


@router.get("/users/{user_id}/posts", response_model=List[post_schema.Post])
def get_all_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    return user_api.find_posts_by_user_id(db, user_id)


@router.get("/users/{user_id}/posts/{post_id}")
def get_post_by_user(user_id: int, post_id: int, db: Session = Depends(get_db)):
    return {}


@router.get("/users/{user_id}/comments")
def get_all_comments_by_user(user_id: int, db: Session = Depends(get_db)):
    return {}


@router.get("/users/{user_id}/comments/{comment_id}")
def get_comment_by_user(user_id: int, comment_id: int, db: Session = Depends(get_db)):
    return {}
