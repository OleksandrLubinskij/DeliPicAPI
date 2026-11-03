from sqlalchemy import select
from typing import Generic, Type, TypeVar, Async
from sqlalchemy.ext.asyncio import AsyncSession

Entity = TypeVar("Entity")

class BaseRepo(Generic[Entity]):
    def __init__(self, db: AsyncSession, entity: Type[Entity]):
        self.db = db
        self.entity = entity

    async def get_all(self, 
                    offset: int,
                    limit: int) -> list[Entity]:
        pass

    async def get_by_id(self, 
                        id: int) -> Entity:
        pass

    async def add(self, 
                  instance: Entity) -> Entity:
        pass

    async def edit(self, 
                   id: int, 
                   new_data: dict) -> Entity:
        pass

    async def delete(self,
                     id: int) -> Entity:
        pass
