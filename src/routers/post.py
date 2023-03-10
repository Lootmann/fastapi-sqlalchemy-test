from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.apis import auth as auth_api
from src.apis import post as post_api
from src.apis import user as user_api
from src.db import get_db
from src.schemas import comment as comment_schema
from src.schemas import post as post_schema
from src.schemas import user as user_schema

router = APIRouter()


@router.get("/posts", response_model=List[post_schema.Post])
def get_all_posts(
    db: Session = Depends(get_db),
    _: user_schema.User = Depends(auth_api.get_current_active_user),
):
    return post_api.get_all_posts(db)


@router.get("/posts/{post_id}", response_model=post_schema.Post)
def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db),
    _: user_schema.User = Depends(auth_api.get_current_active_user),
):
    post = post_api.find_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post:{post_id} Not Found")
    return post


@router.get("/posts/{post_id}/comments", response_model=List[comment_schema.Comment])
def get_comments_by_post_id(
    post_id: int,
    db: Session = Depends(get_db),
    _: user_schema.User = Depends(auth_api.get_current_active_user),
):
    post = post_api.find_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post:{post_id} Not Found")
    return post.comments


@router.post("/posts", response_model=post_schema.PostCreateResponse, status_code=201)
def create_post(
    post_body: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(auth_api.get_current_active_user),
):
    user = user_api.find_user_by_id(db, current_user.id)
    return post_api.create_post(db, user, post_body)


@router.patch(
    "/posts/{post_id}",
    response_model=post_schema.PostCreateResponse,
    status_code=status.HTTP_200_OK,
)
def update_post(
    response: Response,
    post_id: int,
    post_body: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(auth_api.get_current_active_user),
):
    post: post_schema.Post = post_api.find_post_by_id(db, post_id)

    if not post:
        response.status_code = status.HTTP_201_CREATED
        raise HTTPException(status_code=404, detail=f"Post:{post_id} Not Found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=401, detail=f"Not Authenticated")

    return post_api.update_post(db, post, post_body)


@router.delete("/posts/{post_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(auth_api.get_current_active_user),
):
    post = post_api.find_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post:{post_id} Not Found")

    if current_user.id != post.user_id:
        raise HTTPException(status_code=401, detail=f"Not Authenticated")

    return post_api.delete_post(db, post)
