from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from app.database.connection import engine
from app.database.init_db import physical_activity_seeder
from app.core.exceptions import NotFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await physical_activity_seeder()

    try:
        yield
    finally:
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def gingerbread():
    return {"message": "Домашні пряники"}


@app.exception_handler(NotFoundError)
async def not_found(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Not found!"}
    )