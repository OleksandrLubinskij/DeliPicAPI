from fastapi import APIRouter

router = APIRouter(
    prefix="/diary",
    tags=["Diary"]
)

@router.get("/")
async def diary_teapot():
    return {"messsage": "Diary is teapot!"}