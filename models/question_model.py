from pydantic import BaseModel
from typing import List
from datetime import datetime

class QuestionBase(BaseModel):
    quiz_id: str  # The quiz this question belongs to
    question_text: str
    options: List[str]  # List of multiple-choice options
    correct_answer: str  # Correct option from the list
    marks: int  # Added marks field for the question

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: str
    created_at: datetime
    updated_at: datetime  # Added updated_at field

    class Config:
        from_attributes = True
