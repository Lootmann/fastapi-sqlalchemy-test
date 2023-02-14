from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db

router = APIRouter()


@router.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    return {"router p osts": "GET /posts"}


@router.get("/posts/{post_id}")
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    return {"router posts": f"GET /posts/{post_id}"}


@router.get("/posts/{post_id}/comments")
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return {"router posts": f"GET /posts/{post_id}"}


@router.get("/posts/{post_id}/comments/{comment_id}")
def get_comment_by_post(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    return {"router posts": f"GET /posts/{post_id}/comments/{comment_id}"}


@router.post("/posts")
def create_post(db: Session = Depends(get_db)):
    return {"router posts": "POST /posts"}


@router.put("/posts/{post_id}")
def update_post(post_id: int, db: Session = Depends(get_db)):
    return {}


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return {}
