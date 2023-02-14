from fastapi import FastAPI
from src.routers import user as user_router
from src.routers import post as post_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(post_router.router)
