from pydantic import BaseModel

class FullPhysicalActivityResponce(BaseModel):
    id: int
    name: str
    description: str
    activity_ratio: float