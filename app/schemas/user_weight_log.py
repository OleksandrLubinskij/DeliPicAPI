from datetime import datetime

from pydantic import BaseModel

class UserWeightLogModel(BaseModel):
    user_id: int
    weight: float

class FullUserWeightResponce(BaseModel):
    user_id: int
    weight: float
    timestamp: datetime