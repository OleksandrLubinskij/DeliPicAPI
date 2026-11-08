from fastapi import Depends
from services.base_service import BaseCRUDService
from database.models import Diary
from repository.diary_repository import DiaryRepository, get_diary_repo


class DiaryService(BaseCRUDService):
    repo: DiaryRepository
    def __init__(self, repo: DiaryRepository):
        super().__init__(repo)

def get_diary_service(repo: DiaryRepository = Depends(get_diary_repo)) -> DiaryService:
      return DiaryService(repo=repo)