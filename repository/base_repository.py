from sqlalchemy import select
from sqlalchemy.orm import load_only
from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

Entity = TypeVar("Entity")

class BaseRepo(Generic[Entity]):
    def __init__(self, db: AsyncSession, entity: Type[Entity]):
        self.db = db
        self.entity = entity

    async def get_all(self, 
                    offset: int | None = None,
                    limit: int | None = None) -> list[Entity]:
        stmt = select(
            self.entity
            ).offset(
                offset
            ).limit(
                limit)
        result = (await self.db.execute(stmt)).scalars().all()
        return result
    
    async def get_by_id(self, 
                        id: int,
                        fields: list[str] | None = None) -> Entity:
        stmt = select(
            self.entity
        ).where(
            self.entity.id == id
        )

        selected_fields = []
        for field in fields:
            if hasattr(self.entity, field):
                attr = getattr(self.entity, field)
                selected_fields.append(attr)

        stmt = stmt.options(load_only(*selected_fields))

        result = (await self.db.execute(stmt)).sclar()

        return result

    async def add(self, 
                  instance: Entity) -> Entity | None:
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update(self, 
                   id: int, 
                   new_data: dict) -> Entity | None:
        instance = await self.get_by_id(id)
        if not instance:
            return None

        for key, value in new_data.items():
            setattr(instance, key, value)

        return instance

    async def delete(self,
                     id: int) -> Entity | None:
        instance = await self.get_by_id(id)
        if not instance:
            return False

        await self.db.delete(instance)
        return True
