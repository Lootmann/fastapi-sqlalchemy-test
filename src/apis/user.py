from typing import List

from sqlalchemy.orm import Session

from src.schemas import user as user_schema
from src.models import user as user_model


def get_all_users(db: Session) -> List[user_schema.User]:
    return db.query(user_model.User).all()


def get_user_by_id(db: Session, user_id: int) -> user_model.User | None:
    return (
        db.query(user_model.User.id, user_model.User.name)
        .filter(user_model.User.id == user_id)
        .first()
    )


def create_user(
    db: Session, user_body: user_schema.UserCreate
) -> user_model.User:
    user = user_model.User(**user_body.dict())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
