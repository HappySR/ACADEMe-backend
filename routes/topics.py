import uuid
from fastapi import APIRouter, Depends
from services.topic_service import TopicService
from services.material_service import MaterialService
from models.topic_model import TopicCreate, SubtopicCreate
from models.material_model import MaterialCreate
from utils.auth import get_current_user

router = APIRouter(prefix="/courses", tags=["Courses & Topics"])

### 📌 TOPIC ROUTES ###

@router.post("/{course_id}/topics/", response_model=dict)
async def add_topic(course_id: str, topic: TopicCreate, user: dict = Depends(get_current_user)):
    """Adds a topic (chapter) under a specific course with an auto-generated ID."""
    topic_id = str(uuid.uuid4())  # ✅ Auto-generate topic ID
    return await TopicService.create_topic(course_id, topic_id, topic)

@router.get("/{course_id}/topics/", response_model=list)
async def fetch_topics(course_id: str, user: dict = Depends(get_current_user)):
    """Fetches all topics (chapters) under a specific course."""
    return await TopicService.get_all_topics(course_id)


### 📌 SUBTOPIC ROUTES ###

@router.post("/topics/{topic_id}/subtopics/", response_model=dict)
async def add_subtopic(topic_id: str, subtopic: SubtopicCreate, user: dict = Depends(get_current_user)):
    """Adds a subtopic under a specific topic with an auto-generated ID."""
    subtopic_id = str(uuid.uuid4())  # ✅ Auto-generate subtopic ID
    return await TopicService.create_subtopic(topic_id, subtopic_id, subtopic)

@router.get("/topics/{topic_id}/subtopics/", response_model=list)
async def fetch_subtopics(topic_id: str, user: dict = Depends(get_current_user)):
    """Fetches all subtopics under a specific topic."""
    return await TopicService.get_subtopics_by_topic(topic_id)


### 📌 STUDY MATERIAL ROUTES (FOR TOPICS) ###

@router.post("/topics/{topic_id}/materials/", response_model=dict)
async def add_material_to_topic(topic_id: str, material: MaterialCreate, user: dict = Depends(get_current_user)):
    """Adds a study material under a topic."""
    return await MaterialService.add_material(topic_id, material)

@router.get("/topics/{topic_id}/materials/", response_model=list)
async def fetch_materials_from_topic(topic_id: str, user: dict = Depends(get_current_user)):
    """Fetches all study materials under a topic."""
    return await MaterialService.get_materials(topic_id)


### 📌 STUDY MATERIAL ROUTES (FOR SUBTOPICS) ###

@router.post("/topics/{topic_id}/subtopics/{subtopic_id}/materials/", response_model=dict)
async def add_material_to_subtopic(topic_id: str, subtopic_id: str, material: MaterialCreate, user: dict = Depends(get_current_user)):
    """Adds a study material under a subtopic."""
    return await MaterialService.add_material(topic_id, material, is_subtopic=True, subtopic_id=subtopic_id)

@router.get("/topics/{topic_id}/subtopics/{subtopic_id}/materials/", response_model=list)
async def fetch_materials_from_subtopic(topic_id: str, subtopic_id: str, user: dict = Depends(get_current_user)):
    """Fetches all study materials under a subtopic."""
    return await MaterialService.get_materials(topic_id, is_subtopic=True, subtopic_id=subtopic_id)
