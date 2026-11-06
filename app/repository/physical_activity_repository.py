from fastapi import Depends
from database.models import PhysicalActivityInfo
from database.connection import get_async_db
from repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

class PhysicalActivityRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, PhysicalActivityInfo)

def get_physical_activity_repo(db: AsyncSession = Depends(get_async_db)) -> PhysicalActivityRepository:
    return PhysicalActivityRepository(db=db)