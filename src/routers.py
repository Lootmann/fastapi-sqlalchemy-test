from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import get_db
from src import schema as user_schema
from src import api

router = APIRouter()


@router.get("/status")
def server_status():
    return {"status": "seems fine :^)"}


@router.get("/users", response_model=List[user_schema.User])
def get_all_users(db: Session = Depends(get_db)):
    return api.get_all_users(db)


@router.get("/users/{user_id}", response_model=user_schema.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    result = api.get_user_by_id(db, user_id)
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
    return api.create_user(db, user_body)
