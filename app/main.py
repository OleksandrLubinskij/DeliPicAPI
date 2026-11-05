from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.connection import engine
from app.database.init_db import physical_activity_seeder

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

