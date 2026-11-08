from fastapi import APIRouter, Depends
from ..services.physical_activity_service import get_physical_activity_repo, PhysicalActivityService
router = APIRouter(
    prefix="/physical_activity",
    tags=["PhysicalActivity"]
)

@router.get("/teapot")
async def physical_activity_teapot():
    return {"messsage": "PhysicalActivity is teapot!"}

@router.get("/")
async def read_all_records(limit: int = 10,
                offset: int = 0,
                diary_service: PhysicalActivityService = Depends(get_physical_activity_repo)):
    return await diary_service.fetch_all(offset=offset,
                                         limit=limit)

@router.get("/{id}")
async def read_record(id: int,
                  fields: str | None = None,
                  diary_service: PhysicalActivityService = Depends(get_physical_activity_repo)):
    if fields:
        fields = fields.split(",")
        return await diary_service.fetch_by_id(id=id,
                                           fields=fields)
    else:
        return await diary_service.fetch_by_id(id=id)

