from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db

router = APIRouter()


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return {"router users": "get all users"}


@router.get("/users/{user_id}")
def get_post_by_id(user_id: int, db: Session = Depends(get_db)):
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


@router.post("/users")
def create_user(db: Session = Depends(get_db)):
    return {"router users": f"POST /users/"}
