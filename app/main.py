from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from .database.connection import engine
from .database.init_db import physical_activity_seeder, admin_seeder
from .core.exceptions import BaseError

from .v1.routers import user_weight_log
from .v1.routers import diary, physical_activity, product, user, scales
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await physical_activity_seeder()
    await admin_seeder()
    try:
        yield
    finally:
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(product.router)
app.include_router(diary.router)
app.include_router(user_weight_log.router)
app.include_router(physical_activity.router)
app.include_router(scales.router)

@app.get("/")
async def gingerbread():
    return {"message": "Домашні пряники"}


@app.exception_handler(BaseError)
async def base_error_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.error_detail},
    )