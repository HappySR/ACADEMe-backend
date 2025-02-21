from fastapi import APIRouter, HTTPException
from services.quiz_service import create_quiz, get_quizzes_by_topic, get_quizzes_by_subtopic, add_question_to_quiz, get_questions_by_quiz
from models.quiz_model import QuizCreate, QuizResponse, QuestionCreate, QuestionResponse
from typing import List

router = APIRouter()

@router.post("/quizzes/", response_model=QuizResponse)
async def add_quiz(quiz: QuizCreate):
    return create_quiz(quiz)

@router.get("/topics/{topic_id}/quizzes", response_model=List[QuizResponse])
async def fetch_quizzes_by_topic(topic_id: str):
    return get_quizzes_by_topic(topic_id)

@router.get("/subtopics/{subtopic_id}/quizzes", response_model=List[QuizResponse])
async def fetch_quizzes_by_subtopic(subtopic_id: str):
    return get_quizzes_by_subtopic(subtopic_id)

@router.post("/quizzes/{quiz_id}/questions", response_model=QuestionResponse)
async def add_question(quiz_id: str, question: QuestionCreate):
    return add_question_to_quiz(quiz_id, question)

@router.get("/quizzes/{quiz_id}/questions", response_model=List[QuestionResponse])
async def fetch_questions(quiz_id: str):
    return get_questions_by_quiz(quiz_id)
