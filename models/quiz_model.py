from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str  # Subject related to the quiz
    total_marks: int  # Added total_marks for the quiz

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: str
    created_at: datetime
    updated_at: datetime  # Added updated_at field

    class Config:
        from_attributes = True
