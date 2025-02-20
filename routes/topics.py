from fastapi import APIRouter, HTTPException
from services.topic_service import create_topic, get_all_topics, create_subtopic, get_subtopics_by_topic
from models.topic_model import TopicCreate, SubtopicCreate

router = APIRouter()

@router.post("/topics/", response_model=dict)
async def add_topic(topic: TopicCreate):
    return create_topic(topic)

@router.get("/topics/", response_model=list)
async def fetch_all_topics():
    return get_all_topics()

@router.post("/subtopics/", response_model=dict)
async def add_subtopic(subtopic: SubtopicCreate):
    try:
        return create_subtopic(subtopic)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/topics/{topic_id}/subtopics", response_model=list)
async def fetch_subtopics(topic_id: str):
    try:
        return get_subtopics_by_topic(topic_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
