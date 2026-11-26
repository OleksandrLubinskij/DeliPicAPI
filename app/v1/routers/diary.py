from typing import List

from fastapi import APIRouter, Depends
from ...services.diary_service import get_diary_service, DiaryService
from ...schemas.diary import DiaryModel, DiaryUpdate, FullDiaryResponse
from ...schemas.base_response import StatusResonse
from ...core.dependencies import CurrentUserId
from datetime import date 
from ...services.auth_sevice import get_current_user

router = APIRouter(
    prefix="/diary",
    tags=["Diary"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/teapot")
async def diary_teapot():
    return {"messsage": "Diary is teapot!"}

@router.get("/")
async def read_all_records(
    limit: int = 10,
    offset: int = 0,
    diary_service: DiaryService = Depends(get_diary_service)
) -> List[FullDiaryResponse]:
    
    return await diary_service.fetch_all(offset=offset,
                                         limit=limit)

@router.get("/date/{date}")
async def read_all_records_by_date(
    current_user: CurrentUserId,
    target_date: date,
    diary_service:DiaryService = Depends(get_diary_service)
) -> List[FullDiaryResponse]:
    
    return await diary_service.fetch_all_by_date(
        user_id=current_user,
        target_date=target_date
    )

@router.get("/{id}")
async def read_record(
    id: int,
    diary_service: DiaryService = Depends(get_diary_service)
) -> FullDiaryResponse:

        return await diary_service.fetch_by_id(id=id)
 
@router.post("/")
async def create_record(
    diary_data: DiaryModel,
    diary_service: DiaryService = Depends(get_diary_service)
) -> FullDiaryResponse:
    
    result = await diary_service.register(new_data=diary_data)
    return result

@router.patch("/{id}")
async def update_record(
    id: int,
    diary_new_data: DiaryUpdate,
    diary_service: DiaryService = Depends(get_diary_service)
) -> FullDiaryResponse:
    
    result = await diary_service.update(id=id,
                                        new_data=diary_new_data)
    return result

@router.delete("/{id}")
async def delete_record(
    id: int,
    diary_service: DiaryService = Depends(get_diary_service)
) -> StatusResonse:
    await diary_service.remove(id=id)
    return StatusResonse(id=id)