from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.index import app_router, user_router
from src.database.settings import init_database

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def handle_merge_routers():
    app.include_router(app_router)
    app.include_router(user_router)


init_database()
handle_merge_routers()
