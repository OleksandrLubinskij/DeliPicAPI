from datetime import date
from typing import List
from fastapi import APIRouter, Depends
from ...services.user_weight_log_service import get_user_weight_service_service, UserWeightLogService
from ...schemas.user_weight_log import UserWeightLogModel, FullUserWeightResponce
from ...core.dependencies import CurrentUserId

router = APIRouter(
    prefix="/user_weight_log",
    tags=["UserWeightLog"]
)

@router.get("/teapot")
async def user_weight_log_teapot():
    return {"messsage": "UserWeightLog is teapot!"}

@router.get("/")
async def read_user_records_by_period(
    user_id: CurrentUserId,
    start_period: date,
    end_period: date,
    user_weight_log_service: UserWeightLogService = Depends(get_user_weight_service_service)
) -> List[FullUserWeightResponce]:
    return await user_weight_log_service.fetch_by_user_and_id(
        user_id=user_id,
        start_period=start_period,
        end_period=end_period
    )

@router.get("/{id}")
async def read_record(
    id: int,
    user_weight_log_service: UserWeightLogService = Depends(get_user_weight_service_service)
) -> FullUserWeightResponce:
        
    return await user_weight_log_service.fetch_by_id(id=id)

@router.post("/")
async def create_record(
    user_weight_data: UserWeightLogModel,
    user_weight_log_service: UserWeightLogService = Depends(get_user_weight_service_service)
) -> FullUserWeightResponce:
    result = await user_weight_log_service.register(new_data=user_weight_data)
    return result

