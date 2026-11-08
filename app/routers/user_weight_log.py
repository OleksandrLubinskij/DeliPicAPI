from fastapi import APIRouter, Depends
from ..services.user_weight_log_service import get_user_weight_service_service, UserWeightLogService
from ..schemas.user_weight_log import UserWeightLogModel, UserWeightLogUpdate 

router = APIRouter(
    prefix="/user_weight_log",
    tags=["UserWeightLog"]
)

@router.get("/teapot")
async def user_weight_log_teapot():
    return {"messsage": "UserWeightLog is teapot!"}

@router.get("/")
async def read_all_records(limit: int = 10,
                offset: int = 0,
                diary_service: UserWeightLogService = Depends(get_user_weight_service_service)):
    return await diary_service.fetch_all(offset=offset,
                                         limit=limit)

@router.get("/{id}")
async def read_record(id: int,
                  fields: str | None = None,
                  diary_service: UserWeightLogService = Depends(get_user_weight_service_service)):
    if fields:
        fields = fields.split(",")
        return await diary_service.fetch_by_id(id=id,
                                           fields=fields)
    else:
        return await diary_service.fetch_by_id(id=id)

@router.post("/")
async def create_record(diary_data: UserWeightLogModel,
                        diary_service: UserWeightLogService = Depends(get_user_weight_service_service)):
    result = await diary_service.register(new_data=diary_data)
    return result

@router.patch("/{id}")
async def update_record(id: int,
                diary_new_data: UserWeightLogUpdate,
                diary_service: UserWeightLogService = Depends(get_user_weight_service_service)):
    result = await diary_service.update(id=id,
                                        new_data=diary_new_data)
    return result

@router.delete("/{id}")
async def delete_record(id: int,
                  diary_service: UserWeightLogService = Depends(get_user_weight_service_service)):
    return await diary_service.remove(id=id)