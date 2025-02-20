from firebase_admin import firestore
from models.course_model import CourseCreate, CourseResponse
from fastapi import HTTPException

db = firestore.client()

class CourseService:
    @staticmethod
    def create_course(course: CourseCreate):
        """Creates a new course in Firestore."""
        course_ref = db.collection("courses").document(course.id)
        if course_ref.get().exists:
            raise HTTPException(status_code=400, detail="Course already exists")

        course_data = course.dict()
        course_ref.set(course_data)
        return CourseResponse(**course_data)

    @staticmethod
    def get_courses():
        """Fetches all courses from Firestore."""
        courses_ref = db.collection("courses").stream()
        return [doc.to_dict() for doc in courses_ref]
