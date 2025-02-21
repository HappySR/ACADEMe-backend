from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class MaterialCreate(BaseModel):
    type: Literal["text", "image", "audio", "video", "link"]
    category: Literal["Notes", "Reference Links", "Practice Questions"]
    content: str  # URL or text content
    optional_text: Optional[str] = None  # Description of the material

class MaterialResponse(MaterialCreate):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True