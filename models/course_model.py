from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CourseCreate(BaseModel):
    id: str
    title: str
    class_name: str
    description: str
    subject: str  # Added the subject field

class CourseResponse(CourseCreate):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
