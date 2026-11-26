from fastapi import Depends

from ..database.db_enums import UserRole
from ..services.base_service import BaseCRUDService
from ..database.models import User
from ..repository.user_repository import UserRepository, get_user_repo
from ..core.security import get_password_hash, verify_password
from ..schemas.user import UserCreate, UserFromDB, UserOut
class UserService(BaseCRUDService):
    model = User
    repo: UserRepository
    def __init__(self, repo: UserRepository):
        super().__init__(repo)

    async def register(
            self, 
            new_data: UserCreate,
            role: UserRole = UserRole.User.value) -> User:
        plain_password = new_data.password
        hashed_password = await get_password_hash(plain_password=plain_password)

        new_user = User(
            **new_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
            role=role
        )
        created_user = await self.repo.add(new_user)
        return UserOut.model_validate(created_user)

    async def get_user_by_login(self, login: str) -> UserFromDB | None:
        filters = [User.login == login]
        result = await self.repo.get_all(filters=filters)
        if result:
            return UserFromDB.model_validate(result[0])
        return None
    
    async def authenticate(self, login: str, password: str) -> UserFromDB | None:
        user = await self.get_user_by_login(login=login)
        if not user:
             return None
        if not await verify_password(plain_password=password, hashed_password=user.hashed_password):
             return None
        return user

def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
      return UserService(repo=repo)