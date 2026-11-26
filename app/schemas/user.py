from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from ..database.db_enums import UserRole, UserGender

class BaseUser(BaseModel):
    login: str
    email: EmailStr
    gender: UserGender
    weight: float
    height: float
    birth_year: int
    physical_activity: int

class UserModel(BaseUser):
    password: str

class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    gender: Optional[UserGender] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    physical_activity: Optional[int] = None

class UserOut(BaseUser):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class UserFromDB(UserOut):
    hashed_password: str