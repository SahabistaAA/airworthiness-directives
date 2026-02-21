from typing import List, Optional
from pydantic import BaseModel

class Document(BaseModel):
    file_path: str
    filename: str
    text: str
    images: List[str] = []
    metadata: Optional[dict] = {}
