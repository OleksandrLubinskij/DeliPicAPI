from pydantic import BaseModel

class StatusResonse(BaseModel):
    id: int
    status: str = "deleted"