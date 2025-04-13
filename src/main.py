
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "Hello World"}


