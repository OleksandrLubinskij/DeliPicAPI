from fastapi import Depends
from ..database.models import UserWeightLog
from ..database.connection import get_async_db
from ..repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, time, timezone
class UserWeightLogRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, UserWeightLog)

    async def get_by_user_and_period(
            self,
            user_id: int,
            start_period: datetime,
            end_period: datetime
    ) -> list[UserWeightLog]:

        start_dt = datetime.combine(start_period, time.min, tzinfo=timezone.utc)
        end_dt = datetime.combine(end_period, time.max, tzinfo=timezone.utc)
        
        filters = [
            UserWeightLog.user_id == user_id,
            UserWeightLog.timestamp >= start_dt,
            UserWeightLog.timestamp <= end_dt
        ]
        return await super().get_all(filters=filters)
    
def get_user_weight_log_repo(db: AsyncSession = Depends(get_async_db)) -> UserWeightLogRepository:
    return UserWeightLogRepository(db=db)