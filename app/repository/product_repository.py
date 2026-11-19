from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from ..database.models import Product
from ..database.connection import get_async_db
from ..repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, Product)

    async def get_by_embedding(
        self, 
        embedding: List[float], 
        max_distance: float = 0.25 
    ) -> Optional[Product]:
        
        distance = Product.photo_vector.cosine_distance(embedding)
        
        stmt = (
            select(Product)
            .where(Product.photo_vector.is_not(None))
            .where(distance <= max_distance)
            .order_by(distance)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
def get_product_repo(db: AsyncSession = Depends(get_async_db)) -> ProductRepository:
    return ProductRepository(db=db)