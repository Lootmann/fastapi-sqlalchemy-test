from typing import List

from sqlalchemy.orm import Session

from src import schema as user_schema
from src.model import User as user_model


def get_all_users(db: Session) -> List[user_schema.User]:
    return db.query(user_model).all()


def get_user_by_id(db: Session, user_id: int) -> user_model | None:
    return (
        db.query(user_model.id, user_model.name)
        .filter(user_model.id == user_id)
        .first()
    )


def create_user(db: Session, user_body: user_schema.UserCreate) -> user_model:
    user = user_model.User(**user_body.dict())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
