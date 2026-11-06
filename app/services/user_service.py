from fastapi import Depends
from services.base_service import BaseCRUDService
from database.models import User
from repository.user_repository import UserRepository, get_user_repo


class UserService(BaseCRUDService):
    repo: UserRepository
    def __init__(self, repo: UserRepository):
        super().__init__(repo)

def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
      return UserService(repo=repo)