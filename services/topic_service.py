from firebase_admin import firestore
from models.topic_model import TopicCreate, SubtopicCreate
from datetime import datetime
import uuid

db = firestore.client()
topics_collection = db.collection("topics")

def create_topic(topic: TopicCreate):
    topic_id = str(uuid.uuid4())
    new_topic = {
        "id": topic_id,
        "title": topic.title,
        "description": topic.description,
        "created_at": datetime.utcnow()
    }
    topics_collection.document(topic_id).set(new_topic)
    return new_topic

def get_all_topics():
    topics = topics_collection.stream()
    return [topic.to_dict() for topic in topics]

def create_subtopic(subtopic: SubtopicCreate):
    subtopic_id = str(uuid.uuid4())
    topic_ref = topics_collection.document(subtopic.topic_id)

    if not topic_ref.get().exists:
        raise ValueError("Topic not found")

    subtopic_data = {
        "id": subtopic_id,
        "title": subtopic.title,
        "description": subtopic.description,
        "topic_id": subtopic.topic_id,
        "created_at": datetime.utcnow()
    }
    topic_ref.collection("subtopics").document(subtopic_id).set(subtopic_data)
    return subtopic_data

def get_subtopics_by_topic(topic_id: str):
    topic_ref = topics_collection.document(topic_id)
    if not topic_ref.get().exists:
        raise ValueError("Topic not found")

    subtopics = topic_ref.collection("subtopics").stream()
    return [subtopic.to_dict() for subtopic in subtopics]
