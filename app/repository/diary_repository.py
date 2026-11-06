from fastapi import Depends
from database.models import Diary
from database.connection import get_async_db
from repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

class DiaryRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, Diary)

def get_diary_repo(db: AsyncSession = Depends(get_async_db)) -> DiaryRepository:
    return DiaryRepository(db=db)