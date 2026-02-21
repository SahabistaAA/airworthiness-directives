from typing import List
from pydantic import BaseModel

class AircraftConfiguration(BaseModel):
    model: str
    msn: str
    modifications: List[str]