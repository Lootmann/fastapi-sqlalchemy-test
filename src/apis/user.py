from typing import List

from sqlalchemy.orm import Session

from src.schemas import user as user_schema
from src.models import user as user_model


def get_all_users(db: Session) -> List[user_model.User]:
    return db.query(user_model.User).all()


def create_user(db: Session, user_body: user_schema.UserCreate) -> user_model.User:
    user = user_model.User(**user_body.dict())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
