import firebase_admin
from firebase_admin import firestore
from datetime import datetime
from models.topic_model import TopicCreate, SubtopicCreate

db = firestore.client()  # Firestore DB instance

class TopicService:
    @staticmethod
    async def create_topic(course_id: str, topic_id: str, topic: TopicCreate):
        """Creates a new topic inside a course."""
        topic_data = {
            "id": topic_id,  # ✅ Auto-generated topic ID
            "title": topic.title,
            "description": topic.description,
            "created_at": datetime.utcnow()
        }
        db.collection("courses").document(course_id).collection("topics").document(topic_id).set(topic_data)
        return {"message": "Topic created successfully", "topic_id": topic_id}

    @staticmethod
    async def get_all_topics(course_id: str):
        """Fetches all topics for a course."""
        topics_ref = db.collection("courses").document(course_id).collection("topics").stream()
        return [{**topic.to_dict(), "id": topic.id} for topic in topics_ref]

    @staticmethod
    async def create_subtopic(topic_id: str, subtopic_id: str, subtopic: SubtopicCreate):
        """Creates a new subtopic under a topic."""
        topic_doc = db.collection_group("topics").where("id", "==", topic_id).get()
        if not topic_doc:
            return {"error": "Topic not found"}

        subtopic_data = {
            "id": subtopic_id,
            "title": subtopic.title,
            "description": subtopic.description,
            "created_at": datetime.utcnow()
        }
        topic_doc[0].reference.collection("subtopics").document(subtopic_id).set(subtopic_data)
        return {"message": "Subtopic created successfully", "subtopic_id": subtopic_id}

    @staticmethod
    async def get_subtopics_by_topic(topic_id: str):
        """Fetches all subtopics under a topic."""
        topic_doc = db.collection_group("topics").where("id", "==", topic_id).get()
        if not topic_doc:
            return {"error": "Topic not found"}

        subtopics_ref = topic_doc[0].reference.collection("subtopics").stream()
        return [{**subtopic.to_dict(), "id": subtopic.id} for subtopic in subtopics_ref]
