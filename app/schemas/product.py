from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class ProductModel(BaseModel):
    user_id: int
    name: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    photo_path: str | None = None
    photo_vector: List[float] | None = None
    is_accepted: bool

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    photo_path: Optional[str] = None
    is_accepted: Optional[bool] = None

class ProductNutritionResponse(BaseModel):
    id: int
    name: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float

    model_config = ConfigDict(from_attributes=True)