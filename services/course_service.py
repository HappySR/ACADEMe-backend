from firebase_admin import firestore
from models.course_model import CourseCreate, CourseResponse
from fastapi import HTTPException
import uuid
from datetime import datetime  # ✅ Import datetime

db = firestore.client()

class CourseService:
    @staticmethod
    def create_course(course: CourseCreate):
        """Creates a new course in Firestore."""
        course_id = str(uuid.uuid4())  # ✅ Generate UUID here
        course_ref = db.collection("courses").document(course_id)

        if course_ref.get().exists:
            raise HTTPException(status_code=400, detail="Course already exists")

        now = datetime.utcnow()  # ✅ Get current timestamp
        course_data = course.dict()
        course_data["id"] = course_id  # ✅ Assign generated ID
        course_data["created_at"] = now  # ✅ Store timestamps
        course_data["updated_at"] = now  # ✅ Store timestamps

        course_ref.set(course_data)
        return CourseResponse(**course_data)

    @staticmethod
    def get_courses():
        """Fetches all courses from Firestore and adds missing fields if necessary."""
        courses_ref = db.collection("courses").stream()
        
        courses = []
        for doc in courses_ref:
            course_data = doc.to_dict()

            # ✅ Ensure `created_at` and `updated_at` exist (fix missing fields)
            if "created_at" not in course_data or "updated_at" not in course_data:
                course_data["created_at"] = datetime.utcnow()
                course_data["updated_at"] = datetime.utcnow()
                db.collection("courses").document(doc.id).update({
                    "created_at": course_data["created_at"],
                    "updated_at": course_data["updated_at"],
                })

            courses.append(CourseResponse(**course_data))  # ✅ Ensure response matches model

        return courses
