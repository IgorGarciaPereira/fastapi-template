from fastapi import FastAPI

from src.routes.index import app_router


app = FastAPI()


def handle_merge_routers():
    app.include_router(app_router)


handle_merge_routers()
