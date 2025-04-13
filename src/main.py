import logging
import sys

from fastapi import FastAPI, Request

from .routers import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

app = FastAPI()
app.include_router(router)


@app.get("/")
async def index(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "message": "Welcome to the Partventory",
        "docs": f"{base_url}/docs",
        "redoc": f"{base_url}/redoc",
    }
