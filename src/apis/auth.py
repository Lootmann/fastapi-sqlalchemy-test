from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.apis import user as user_api
from src.db import get_db
from src.models import user as user_model
from src.schemas import auth as auth_schema
from src.schemas import user as user_schema
from src.settings import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credential = Settings()


def get_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oath2_scheme),
) -> user_model.User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"wWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, credential.secret_key, algorithms=[credential.algorithm])
        username: str = payload.get("sub", None)

        if username is None:
            raise credential_exception

        token_data = auth_schema.TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = user_api.find_user_by_name(db, token_data.username)

    if user is None:
        raise credential_exception

    return user


def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
    # TODO: check active or not
    # TODO: what is the definition of this 'active'?
    return current_user


def create_access_token(data: dict, expired_delta: timedelta | None = None):
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, credential.secret_key, algorithm=credential.algorithm)

    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str):
    user = user_api.find_user_by_name(db, username)
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user
