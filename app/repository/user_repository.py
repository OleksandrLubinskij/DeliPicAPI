from fastapi import Depends
from ..database.models import User
from ..database.connection import get_async_db
from ..repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

def get_user_repo(db: AsyncSession = Depends(get_async_db)) -> UserRepository:
    return UserRepository(db=db)