from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from .database.connection import engine
from .database.init_db import physical_activity_seeder
from .core.exceptions import NotFoundError

from .v1.routers import user_weight_log
from .v1.routers import diary, physical_activity, product, user
@asynccontextmanager
async def lifespan(app: FastAPI):
    await physical_activity_seeder()

    try:
        yield
    finally:
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(diary.router)
app.include_router(user_weight_log.router)
app.include_router(physical_activity.router)

@app.get("/")
async def gingerbread():
    return {"message": "Домашні пряники"}


@app.exception_handler(NotFoundError)
async def not_found(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Not found!"}
    )