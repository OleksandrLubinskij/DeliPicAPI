from typing import List
from fastapi import Depends
from ..services.base_service import BaseCRUDService
from ..database.models import Diary
from ..repository.diary_repository import DiaryRepository, get_diary_repo
from datetime import date
from ..schemas.diary import DiaryModel, DiaryUpdate

class DiaryService(BaseCRUDService[Diary, DiaryModel, DiaryUpdate]):
    model = Diary 
    repo: DiaryRepository
    def __init__(self, repo: DiaryRepository):
        super().__init__(repo)

    async def fetch_all_by_date(
              self,
              user_id: int,
              target_date: date
              ) -> List[Diary]:
        
        return await self.repo.get_all_by_date(
             user_id=user_id,
             target_date=target_date
        )
    
def get_diary_service(repo: DiaryRepository = Depends(get_diary_repo)) -> DiaryService:
      return DiaryService(repo=repo)