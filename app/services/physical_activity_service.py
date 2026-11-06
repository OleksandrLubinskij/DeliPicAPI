from fastapi import Depends
from services.base_service import BaseCRUDService
from database.models import PhysicalActivityInfo
from repository.physical_activity_repository import PhysicalActivityRepository, get_physical_activity_repo


class PhysicalActivityService(BaseCRUDService):
    repo: PhysicalActivityRepository
    def __init__(self, repo: PhysicalActivityRepository):
        super().__init__(repo)

def get_user_service(repo: PhysicalActivityRepository = Depends(get_physical_activity_repo)) -> PhysicalActivityService:
      return PhysicalActivityService(repo=repo)