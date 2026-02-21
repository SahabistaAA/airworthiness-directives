from typing import List, Optional
from pydantic import BaseModel

class AircraftConfiguration(BaseModel):
    model: str
    msn: str
    modifications: List[str] = []