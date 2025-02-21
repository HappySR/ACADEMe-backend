from firebase_admin import firestore
from models.quiz_model import QuizCreate, QuestionCreate
from datetime import datetime
import uuid

db = firestore.client()
quizzes_collection = db.collection("quizzes")

def create_quiz(quiz: QuizCreate):
    quiz_id = str(uuid.uuid4())
    if quiz.topic_id and quiz.subtopic_id:
        raise ValueError("Quiz cannot belong to both a topic and a subtopic.")
    
    new_quiz = {
        "id": quiz_id,
        "title": quiz.title,
        "description": quiz.description,
        "subject": quiz.subject,
        "topic_id": quiz.topic_id,
        "subtopic_id": quiz.subtopic_id,
        "created_at": datetime.utcnow()
    }
    quizzes_collection.document(quiz_id).set(new_quiz)
    return new_quiz

def get_quizzes_by_topic(topic_id: str):
    quizzes = quizzes_collection.where("topic_id", "==", topic_id).stream()
    return [quiz.to_dict() for quiz in quizzes]

def get_quizzes_by_subtopic(subtopic_id: str):
    quizzes = quizzes_collection.where("subtopic_id", "==", subtopic_id).stream()
    return [quiz.to_dict() for quiz in quizzes]

def add_question_to_quiz(quiz_id: str, question: QuestionCreate):
    quiz_ref = quizzes_collection.document(quiz_id)
    if not quiz_ref.get().exists:
        raise ValueError("Quiz not found")

    question_id = str(uuid.uuid4())
    question_data = {
        "id": question_id,
        "quiz_id": quiz_id,
        "question_text": question.question_text,
        "options": question.options,
        "correct_answer": question.correct_answer,
        "created_at": datetime.utcnow()
    }
    quiz_ref.collection("questions").document(question_id).set(question_data)
    return question_data

def get_questions_by_quiz(quiz_id: str):
    quiz_ref = quizzes_collection.document(quiz_id)
    if not quiz_ref.get().exists:
        raise ValueError("Quiz not found")

    questions = quiz_ref.collection("questions").stream()
    return [question.to_dict() for question in questions]
