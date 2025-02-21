from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    id: str
    title: str
    course_id: str
    class_name: str

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
    id: str
    title: str
    topic_id: str
    course_id: str
    class_name: str

class SubtopicResponse(SubtopicBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
