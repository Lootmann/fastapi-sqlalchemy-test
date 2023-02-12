from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(BaseModel):
    pass


class UserCreateResponse(UserCreate):
    id: int
