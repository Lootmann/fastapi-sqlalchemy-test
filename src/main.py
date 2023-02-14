from fastapi import FastAPI
from src.routers import user as user_router
from src.routers import post as post_router
from src.routers import comment as comment_router
from src.routers import root as root_router

app = FastAPI()
app.include_router(root_router.router)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
