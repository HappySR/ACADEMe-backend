from firebase_admin import firestore
from models.question_model import QuestionCreate, QuestionResponse
from datetime import datetime
import uuid
from fastapi import HTTPException

db = firestore.client()
quizzes_collection = db.collection("quizzes")

def create_question(question: QuestionCreate):
    """Creates a new question inside a quiz in Firestore."""
    question_id = str(uuid.uuid4())
    quiz_ref = quizzes_collection.document(question.quiz_id)

    if not quiz_ref.get().exists:
        raise HTTPException(status_code=404, detail="Quiz not found")

    question_data = {
        "id": question_id,
        "quiz_id": question.quiz_id,
        "question_text": question.question_text,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "class": question.class_,
        "created_at": datetime.utcnow()
    }
    quiz_ref.collection("questions").document(question_id).set(question_data)
    return QuestionResponse(**question_data)

def get_questions_by_quiz(quiz_id: str):
    """Fetches questions belonging to a specific quiz."""
    quiz_ref = quizzes_collection.document(quiz_id)

    if not quiz_ref.get().exists:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = quiz_ref.collection("questions").stream()
    return [question.to_dict() for question in questions]
