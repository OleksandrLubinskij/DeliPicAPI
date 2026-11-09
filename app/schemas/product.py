from pydantic import BaseModel
from typing import Optional, List

class ProductModel(BaseModel):
    user_id: int
    title: str
    calories: float
    proteins: float
    carbohydrates: float
    fats: float
    photo_path: str
    photo_vector: List[float]
    is_accepted: bool

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    photo_path: Optional[str] = None
    photo_vector: Optional[List[float]] = None