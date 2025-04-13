from fastapi import FastAPI

from .database import engine, Base
from .routers import router


app = FastAPI()
app.include_router(router)


@app.get("/")
def index():
    return {"message": "Hello World"}
