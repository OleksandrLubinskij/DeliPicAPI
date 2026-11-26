from .connection import async_session_maker
from .models import PhysicalActivityInfo
from sqlalchemy import select
from .seed_data import physical_activity_items
from ..repository.user_repository import User, UserRepository
from .db_enums import UserRole, UserGender
from ..services.user_service import UserService
from ..schemas.user import UserCreate
from ..core.config import admin_account

async def physical_activity_seeder():
    async with async_session_maker() as session:
        result = await session.execute(select(PhysicalActivityInfo).limit(1))

        if not result.scalars().first():
            items_to_add = [PhysicalActivityInfo(**data) for data in physical_activity_items]

            session.add_all(items_to_add)
            await session.commit()
            print("\nPhysical activity ratios added!\n")
        else:
            print("\nPhysical activity coefficients have already been created!\n")

async def admin_seeder():
    async with async_session_maker() as session:
        stmt = select(User).where(User.role == UserRole.Admin.value).limit(1)
        result = await session.execute(stmt)

    if result.scalars().first():
        print("Admin account already exists!")
        return
    
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)

    admin_user = UserCreate(
        login=admin_account.login.get_secret_value(),
        email=admin_account.email.get_secret_value(),
        password=admin_account.email.get_secret_value(),
        gender=UserGender.Male.value,
        weight=80,
        height=170,
        birth_year=2000,
        physical_activity=1
    )
    await user_service.register(new_data=admin_user, role=UserRole.Admin.value)
    print("Admin user created successfully!")


         