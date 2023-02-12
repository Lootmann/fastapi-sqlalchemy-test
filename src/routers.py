from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {"hello": "world"}


@router.get("/users")
def get_all_users():
    return {"users": "users"}
