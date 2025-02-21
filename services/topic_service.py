from firebase_admin import firestore
from models.topic_model import TopicCreate, SubtopicCreate
from fastapi import HTTPException
import uuid
from datetime import datetime

db = firestore.client()

class TopicService:
    @staticmethod
    def create_topic(topic: TopicCreate):
        """Creates a topic (chapter) under a course."""
        course_ref = db.collection("courses").document(topic.course_id)
        if not course_ref.get().exists:
            raise HTTPException(status_code=404, detail="Course not found")

        topic_id = str(uuid.uuid4())
        topic_data = {
            "id": topic_id,
            "title": topic.title,
            "description": topic.description,
            "created_at": datetime.utcnow()
        }

        course_ref.collection("topics").document(topic_id).set(topic_data)
        return topic_data

    @staticmethod
    def get_all_topics(course_id: str):
        """Fetches all topics under a specific course."""
        course_ref = db.collection("courses").document(course_id)
        if not course_ref.get().exists:
            raise HTTPException(status_code=404, detail="Course not found")

        topics_ref = course_ref.collection("topics").stream()
        return [topic.to_dict() for topic in topics_ref]

    @staticmethod
    def create_subtopic(subtopic: SubtopicCreate):
        """Creates a subtopic (topic under a chapter)."""
        course_ref = db.collection("courses").document(subtopic.course_id)
        topic_ref = course_ref.collection("topics").document(subtopic.topic_id)

        if not topic_ref.get().exists:
            raise HTTPException(status_code=404, detail="Topic not found")

        subtopic_id = str(uuid.uuid4())
        subtopic_data = {
            "id": subtopic_id,
            "title": subtopic.title,
            "description": subtopic.description,
            "created_at": datetime.utcnow()
        }

        topic_ref.collection("subtopics").document(subtopic_id).set(subtopic_data)
        return subtopic_data

    @staticmethod
    def get_subtopics_by_topic(course_id: str, topic_id: str):
        """Fetches all subtopics under a topic."""
        course_ref = db.collection("courses").document(course_id)
        topic_ref = course_ref.collection("topics").document(topic_id)

        if not topic_ref.get().exists:
            raise HTTPException(status_code=404, detail="Topic not found")

        subtopics_ref = topic_ref.collection("subtopics").stream()
        return [subtopic.to_dict() for subtopic in subtopics_ref]
