from fastapi import APIRouter

router = APIRouter(
    prefix="/user_weight_log",
    tags=["UserWeightLog"]
)

@router.get("/")
async def user_weight_log_teapot():
    return {"messsage": "UserWeightLog is teapot!"}