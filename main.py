from fastapi import FastAPI

from src.routes.index import app_router, user_router
from src.database.settings import init_database

app = FastAPI()


def handle_merge_routers():
    app.include_router(app_router)
    app.include_router(user_router)


init_database()
handle_merge_routers()
