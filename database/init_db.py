from .connection import async_session_maker
from .models import PhysicalActivityInfo
from sqlalchemy import select
from .seed_data import physical_activity_items

async def physical_activity_seeder():
    async with async_session_maker() as session:
        result = await session.execute(select(PhysicalActivityInfo).limit(1))

        if not result.scalars().first():
            items_to_add = [PhysicalActivityInfo(**data) for data in physical_activity_items]

            session.add_all(items_to_add)
            await session.commit()
            print("\nКоефіцієнти фізичної активності додано!\n")
        else:
            print("\nКоефіцієнти фізичної активності уже створено!\n")