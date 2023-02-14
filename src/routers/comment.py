from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db


router = APIRouter()


@router.get("/comments")
def get_all_comments(db: Session = Depends(get_db)):
    return {"router comments": "GET /comments"}


@router.get("/comments/{comment_id}")
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    return {"router comments": f"GET /comments/{comment_id}"}


@router.post("/comments")
def create_comment(db: Session = Depends(get_db)):
    return {"router comments": "POST/comments"}
