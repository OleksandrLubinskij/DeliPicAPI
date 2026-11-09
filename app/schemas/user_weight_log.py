from pydantic import BaseModel
from typing import Optional

class UserWeightLogModel(BaseModel):
    user_id: int
    weight: float