from fastapi import APIRouter

app_router = APIRouter()


@app_router.get('/')
def read_root():
    return {"Hello": "World"}
