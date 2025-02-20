from fastapi import APIRouter, Depends, HTTPException
from services.question_service import create_question, get_questions_by_quiz
from models.question_model import QuestionCreate, QuestionResponse
from utils.auth import get_current_user
from utils.class_filter import filter_questions_by_class

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/", response_model=QuestionResponse)
async def add_question(question: QuestionCreate, user: dict = Depends(get_current_user)):
    """Adds a new question to a quiz (admin-only feature in the future)."""
    try:
        return create_question(question)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/quiz/{quiz_id}", response_model=list[QuestionResponse])
async def fetch_questions(quiz_id: str, user: dict = Depends(get_current_user)):
    """Fetches all questions for a given quiz, filtered by the user’s selected class."""
    try:
        all_questions = get_questions_by_quiz(quiz_id)
        return filter_questions_by_class(all_questions, user["class"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
