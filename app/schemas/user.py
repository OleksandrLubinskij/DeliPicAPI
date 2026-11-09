from pydantic import BaseModel
from typing import Optional
from ..database.db_enums import UserRole, UserGender

class UserModel(BaseModel):
    role: UserRole
    login: str
    password: str
    gender: UserGender
    weight: float
    height: float
    birth_year: int
    physical_activity: int

class UserUpdate(BaseModel):
    login: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[UserGender] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    physical_activity: Optional[int] = None