from firebase_admin import firestore
from models.quiz_model import QuizCreate, QuizResponse
from datetime import datetime
import uuid

db = firestore.client()
quizzes_collection = db.collection("quizzes")

def create_quiz(quiz: QuizCreate):
    """Creates a new quiz in Firestore."""
    quiz_id = str(uuid.uuid4())
    new_quiz = {
        "id": quiz_id,
        "title": quiz.title,
        "description": quiz.description,
        "subject": quiz.subject,
        "class": quiz.class_,
        "created_at": datetime.utcnow()
    }
    quizzes_collection.document(quiz_id).set(new_quiz)
    return QuizResponse(**new_quiz)

def get_all_quizzes():
    """Fetches all quizzes from Firestore."""
    quizzes = quizzes_collection.stream()
    return [quiz.to_dict() for quiz in quizzes]
