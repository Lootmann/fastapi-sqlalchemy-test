from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas import user as user_schema
from src.apis import user as user_api
from src.db import get_db

router = APIRouter()


@router.get("/users", response_model=List[user_schema.User])
def get_all_users(db: Session = Depends(get_db)):
    return user_api.get_all_users(db)


@router.post("/users", response_model=user_schema.UserCreateResponse)
def create_user(user_body: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_api.create_user(db, user_body)


@router.put("/users/{user_id}", response_model=user_schema.UserCreateResponse)
def update_user(user_id: int, user_body: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_api.find_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User:{user_id} Not Found")
    return user_api.update_user(db, user, user_body)


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return {"router users": f"GET /users/{user_id}"}


@router.get("/users/{user_id}/posts")
def get_all_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    return {"router users": f"GET /users/{user_id}/posts"}


@router.get("/users/{user_id}/posts/{post_id}")
def get_post_by_user(user_id: int, post_id: int, db: Session = Depends(get_db)):
    return {"router users": f"GET /users/{user_id}/posts/{post_id}"}


@router.get("/users/{user_id}/comments")
def get_all_comments_by_user(user_id: int, db: Session = Depends(get_db)):
    return {"router users": f"GET /users/{user_id}/comments"}


@router.get("/users/{user_id}/comments/{comment_id}")
def get_comment_by_user(user_id: int, comment_id: int, db: Session = Depends(get_db)):
    return {"router users": f"GET /users/{user_id}/comments/{comment_id}"}
