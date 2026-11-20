from pydantic import BaseModel
from typing import Optional

class DiaryModel(BaseModel):
    user_id: int
    product_name_snapshot: str
    product_id: int
    weight: float
    calories_consumed: float
    proteins_consumed: float
    carbohydrates_consumed: float
    fats_consumed: float

class DiaryUpdate(BaseModel):
    product_id: Optional[int] = None
    weight: Optional[float] = None

class SaveToDiaryRequest(BaseModel):
    product_id: int
    product_name: str
    weight: float
    calories: float
    proteins: float
    carbohydrates: float
    fats: float