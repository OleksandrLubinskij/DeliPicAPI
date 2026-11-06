from fastapi import Depends
from database.models import Product
from database.connection import get_async_db
from repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, Product)

def get_product_repo(db: AsyncSession = Depends(get_async_db)) -> ProductRepository:
    return ProductRepository(db=db)