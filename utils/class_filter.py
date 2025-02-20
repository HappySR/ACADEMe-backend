from firebase_admin import firestore

db = firestore.client()

def filter_courses_by_class(courses: list, student_class: str):
    """Filters courses based on the user's selected class."""
    return [course for course in courses if course.get("class") == student_class]

def filter_quizzes_by_class(quizzes: list, student_class: str):
    """Filters quizzes based on the user's selected class."""
    return [quiz for quiz in quizzes if quiz.get("class") == student_class]

def filter_questions_by_class(questions: list, student_class: str):
    """Filters questions based on the user's selected class."""
    return [question for question in questions if question.get("class") == student_class]
