from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicResponse(TopicBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class SubtopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    topic_id: str  # Reference to parent topic

class SubtopicCreate(SubtopicBase):
    pass

class SubtopicResponse(SubtopicBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
