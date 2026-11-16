from fastapi import Depends
from typing import Any, Sequence
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
                      limit: int | None = None,) -> list[Product]:
        options = (defer(Product.photo_vector),)

        return await super().get_all(offset=offset,
                                    limit=limit,
                                    options=options)
    
    async def get_by_id(self, 
                        id: int,
                        fields: list[str] | None = None,
                        include_embedding: bool = False) -> Product:
        
        options = () if include_embedding else (defer(Product.photo_vector),)
        return await super().get_by_id(id=id,
                                    fields=fields,
                                    options=options)
    
def get_product_repo(db: AsyncSession = Depends(get_async_db)) -> ProductRepository:
    return ProductRepository(db=db)