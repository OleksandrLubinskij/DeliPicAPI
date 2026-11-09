from fastapi import Depends
from ..database.models import UserWeightLog
from ..database.connection import get_async_db
from ..repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

class UserWeightLogRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, UserWeightLog)

def get_user_weight_log_repo(db: AsyncSession = Depends(get_async_db)) -> UserWeightLogRepository:
    return UserWeightLogRepository(db=db)