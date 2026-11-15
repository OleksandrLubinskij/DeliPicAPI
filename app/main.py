from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from .database.connection import engine
from .database.init_db import physical_activity_seeder
from .core.exceptions import NotFoundError, ServiceUnavailable, InvalidPhoto, RecognitionFailed

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

@app.exception_handler(ServiceUnavailable)
async def service_unavailable(request: Request, exc: ServiceUnavailable):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": exc.error_detail or "Service is temporarily unavailable"
        },
    )

@app.exception_handler(InvalidPhoto)
async def invalid_photo(request: Request, exc: InvalidPhoto):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.error_detail
        }
    )

@app.exception_handler(RecognitionFailed)
async def recognition_failed(request: Request, exc: RecognitionFailed):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": exc.error_detail
        }
    )