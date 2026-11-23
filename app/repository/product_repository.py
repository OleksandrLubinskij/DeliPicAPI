from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from ..database.models import Product
from ..database.connection import get_async_db
from ..repository.base_repository import BaseRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

class ProductRepository(BaseRepo):   
    def __init__(self, db: AsyncSession):
        super().__init__(db, Product)

    async def get_all(self, 
                      offset: int | None = None,
                      limit: int | None = None,
                      is_accept_state: bool | None = None
                      ) -> list[Product]:
        
        options = (defer(Product.photo_vector),)
        filters = [Product.is_accepted == is_accept_state]
        
        return await super().get_all(offset=offset,
                                    limit=limit,
                                    options=options,
                                    filters=filters)
    
    async def get_by_id(self, 
                        id: int,
                        fields: list[str] | None = None,
                        include_embedding: bool = False) -> Product:
        
        options = () if include_embedding else (defer(Product.photo_vector),)
        return await super().get_by_id(id=id,
                                    fields=fields,
                                    options=options)
    
    async def get_by_embedding(
        self, 
        user_id: int,
        embedding: List[float], 
        max_distance: float = 0.12 
    ) -> Optional[Product]:
        
        distance = Product.photo_vector.cosine_distance(embedding)

        user_stmt = (
            select(Product)
            .where(Product.photo_vector.is_not(None))
            .where(distance <= max_distance)
            .where(Product.user_id == user_id)
            .order_by(distance)
            .limit(1)
        )

        product = (await self.db.execute(user_stmt)).scalar_one_or_none()
        if product:
            return product

        global_stmt = (
            select(Product)
            .where(Product.photo_vector.is_not(None))
            .where(distance <= max_distance)
            .where(Product.user_id != user_id)
            .where(Product.is_accepted.is_(True))
            .order_by(distance)
            .limit(1)
        )
        return (await self.db.execute(global_stmt)).scalar_one_or_none()
        
        
def get_product_repo(db: AsyncSession = Depends(get_async_db)) -> ProductRepository:
    return ProductRepository(db=db)