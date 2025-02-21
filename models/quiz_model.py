from pydantic import BaseModel
from typing import Optional, List

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    topic_id: Optional[str] = None  # Quiz can belong to either a topic or a subtopic
    subtopic_id: Optional[str] = None  # If this is set, topic_id should be None

class QuizResponse(QuizCreate):
    id: str

class QuestionCreate(BaseModel):
    question_text: str
    options: List[str]
    correct_answer: str

class QuestionResponse(QuestionCreate):
    id: str
    quiz_id: str
