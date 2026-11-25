from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from ..database.db_enums import MealType

class DiaryModel(BaseModel):
    user_id: int
    product_name_snapshot: str
    product_id: int
    weight: float
    calories_consumed: float
    proteins_consumed: float
    carbohydrates_consumed: float
    fats_consumed: float
    meal_type: MealType

class DiaryUpdate(BaseModel):
    product_id: Optional[int] = None
    weight: Optional[float] = None
    meal_type: Optional[MealType] = None

class SaveToDiaryRequest(BaseModel):
    product_id: int
    product_name: str
    weight: float
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    meal_type: MealType

class FullDiaryResponse(BaseModel):
    id: int
    product_name_snapshot: str
    product_id: int | None = None
    user_id: int
    weight: float
    calories_consumed: float
    proteins_consumed: float
    carbohydrates_consumed: float
    fats_consumed: float
    meal_type: MealType
    timestamp: datetime
