from typing import List

from fastapi import APIRouter, Depends
from ...services.physical_activity_service import get_physical_activity_service, PhysicalActivityService
from ...schemas.physical_activity import FullPhysicalActivityResponce

router = APIRouter(
    prefix="/physical_activity",
    tags=["PhysicalActivity"]
)

@router.get("/teapot")
async def physical_activity_teapot():
    return {"messsage": "PhysicalActivity is teapot!"}

@router.get("/")
async def read_all_records(
    limit: int = 10,
    offset: int = 0,
    physical_activity_service: PhysicalActivityService = Depends(get_physical_activity_service)
) -> List[FullPhysicalActivityResponce]:
    
    return await physical_activity_service.fetch_all(
        offset=offset,
        limit=limit)

@router.get("/{id}")
async def read_record(
    id: int,
    physical_activity_service: PhysicalActivityService = Depends(get_physical_activity_service)
) -> FullPhysicalActivityResponce:
        
        return await physical_activity_service.fetch_by_id(id=id)

