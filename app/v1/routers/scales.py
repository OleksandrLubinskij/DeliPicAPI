from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/scales",
    tags=["Scales"]
)

@router.get("/teapot")
async def scale_teapot():
    return {"messsage": "Scale is teapot!"}