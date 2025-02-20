from fastapi import APIRouter, Depends, HTTPException
from services.quiz_service import create_quiz, get_all_quizzes
from models.quiz_model import QuizCreate, QuizResponse
from utils.auth import get_current_user
from utils.class_filter import filter_quizzes_by_class

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/", response_model=QuizResponse)
async def add_quiz(quiz: QuizCreate, user: dict = Depends(get_current_user)):
    """Adds a new quiz (admin-only feature in the future)."""
    created_quiz = create_quiz(quiz)
    if not created_quiz:
        raise HTTPException(status_code=400, detail="Quiz creation failed")
    return created_quiz

@router.get("/", response_model=list[QuizResponse])
async def fetch_all_quizzes(user: dict = Depends(get_current_user)):
    """Fetches all quizzes filtered by the user’s selected class."""
    all_quizzes = get_all_quizzes()
    return filter_quizzes_by_class(all_quizzes, user["class"])
