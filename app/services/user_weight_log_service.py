from fastapi import Depends
from services.base_service import BaseCRUDService
from database.models import UserWeightLog
from repository.user_weight_log_repository import UserWeightLogRepository, get_user_weight_log_repo


class UserWeightLogService(BaseCRUDService):
    repo: UserWeightLogRepository
    def __init__(self, repo: UserWeightLogRepository):
        super().__init__(repo)

def get_user_weight_service_service(repo: UserWeightLogRepository = Depends(get_user_weight_log_repo)) -> UserWeightLogService:
      return UserWeightLogService(repo=repo)