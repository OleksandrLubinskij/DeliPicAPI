from fastapi import APIRouter

router = APIRouter(
    prefix="/physical_activity",
    tags=["PhysicalActivity"]
)

@router.get("/")
async def physical_activity_teapot():
    return {"messsage": "PhysicalActivity is teapot!"}