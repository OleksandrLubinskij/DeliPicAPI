from fastapi import Depends
from ..database.models import Diary
from ..database.connection import get_async_db
from ..repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date,  time, timedelta

class DiaryRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, Diary)

    async def get_all_by_date(self, 
                        user_id: int,
                        target_date: date
                    ) -> list[Diary]:
        start_of_day = datetime.combine(target_date, time.min)
        end_of_day = start_of_day + timedelta(days=1)
        filters = [
            Diary.user_id == user_id,
            Diary.timestamp >= start_of_day,
            Diary.timestamp < end_of_day
        ]
        return await super().get_all(filters=filters)
    
def get_diary_repo(db: AsyncSession = Depends(get_async_db)) -> DiaryRepository:
    return DiaryRepository(db=db)