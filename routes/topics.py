from fastapi import APIRouter, HTTPException, Depends
from services.topic_service import TopicService
from models.topic_model import TopicCreate, SubtopicCreate
from utils.auth import get_current_user

router = APIRouter(prefix="/courses", tags=["Courses & Topics"])

@router.post("/{course_id}/topics/", response_model=dict)
async def add_topic(course_id: str, topic: TopicCreate, user: dict = Depends(get_current_user)):
    """Adds a topic (chapter) under a specific course."""
    return TopicService.create_topic(course_id, topic)

@router.get("/{course_id}/topics/", response_model=list)
async def fetch_topics(course_id: str, user: dict = Depends(get_current_user)):
    """Fetches all topics (chapters) under a specific course."""
    return TopicService.get_all_topics(course_id)

@router.post("/{course_id}/topics/{topic_id}/subtopics/", response_model=dict)
async def add_subtopic(course_id: str, topic_id: str, subtopic: SubtopicCreate, user: dict = Depends(get_current_user)):
    """Adds a subtopic under a specific topic."""
    try:
        return TopicService.create_subtopic(course_id, topic_id, subtopic)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{course_id}/topics/{topic_id}/subtopics/", response_model=list)
async def fetch_subtopics(course_id: str, topic_id: str, user: dict = Depends(get_current_user)):
    """Fetches all subtopics under a specific topic."""
    try:
        return TopicService.get_subtopics_by_topic(course_id, topic_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
