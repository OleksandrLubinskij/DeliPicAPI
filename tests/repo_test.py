import asyncio
from typing import Generic, Sequence, Type, TypeVar
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, load_only, mapped_column

# --- 1. ТЕСТОВА МОДЕЛЬ ---


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))


# --- 2. ВАШ ВІДКОРИГОВАНИЙ РЕПОЗИТОРІЙ ---

Entity = TypeVar("Entity")


class BaseRepo(Generic[Entity]):

    def __init__(self, db: AsyncSession, entity: Type[Entity]):
        self.db = db
        self.entity = entity

    async def get_all(
        self, offset: int | None = None, limit: int | None = None
    ) -> Sequence[Entity]:
        stmt = select(self.entity).offset(offset).limit(limit)
        result = await self.db.scalars(stmt)
        return result.all()

    async def get_by_id(
        self, id: int, fields: list[str] | None = None
    ) -> Entity | None:
        stmt = select(self.entity).where(self.entity.id == id)

        if fields:
            selected_fields = [
                getattr(self.entity, field)
                for field in fields
                if hasattr(self.entity, field)
            ]
            if selected_fields:
                stmt = stmt.options(load_only(*selected_fields))

        return await self.db.scalar(stmt)

    async def add(self, instance: Entity) -> Entity:
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update(self, id: int, new_data: dict) -> Entity | None:
        instance = await self.get_by_id(id)
        if not instance:
            return None

        for key, value in new_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete(self, id: int) -> bool:
        instance = await self.get_by_id(id)
        if not instance:
            return False

        await self.db.delete(instance)
        await self.db.flush()
        return True


# --- 3. СЦЕНАРІЙ ТЕСТУВАННЯ ---


async def main():
    # Створюємо асинхронний двигун SQLite в пам'яті (echo=True покаже згенеровані SQL-запити)
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)

    # Створюємо таблиці у тимчасовій БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        repo = BaseRepo(session, User)

        print("\n=== 1. ТЕСТ: ADD ===")
        user = User(name="Олександр", email="alex@example.com")
        created_user = await repo.add(user)
        print(f"Створено користувача з ID: {created_user.id}")

        print("\n=== 2. ТЕСТ: GET_BY_ID (ПОВНИЙ ОБ'ЄКТ) ===")
        fetched = await repo.get_by_id(created_user.id)
        print(f"Знайдено: id={fetched.id}, name={fetched.name}, email={fetched.email}")

        print("\n=== 3. ТЕСТ: GET_BY_ID (З LOAD_ONLY) ===")
        partial = await repo.get_by_id(created_user.id, fields=["name"])
        print(f"Знайдено тільки name: {partial.name}")

        print("\n=== 4. ТЕСТ: UPDATE ===")
        updated = await repo.update(
            created_user.id, {"name": "Олександр Оновлений"}
        )
        print(f"Оновлено ім'я на: {updated.name}")

        print("\n=== 5. ТЕСТ: GET_ALL ===")
        all_users = await repo.get_all()
        print(f"Усього записів у БД: {len(all_users)}")

        print("\n=== 6. ТЕСТ: DELETE ===")
        is_deleted = await repo.delete(created_user.id)
        print(f"Видалено успішно: {is_deleted}")

        not_found = await repo.get_by_id(created_user.id)
        print(f"Спроба знайти після видалення: {not_found}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())