from pydantic import BaseModel
from typing import Optional

class DiaryModel(BaseModel):
    user_id: int
    product_name: str
    product_id: int
    weight: float
    calories_consumed: float
    proteins_consumed: float
    carbohydrates_consumed: float
    fats_consumed: float

class DiaryUpdate(BaseModel):
    product_id: Optional[int] = None
    weight: Optional[float] = None
