from firebase_admin import firestore
from models.material_model import MaterialCreate, MaterialResponse
from datetime import datetime
import uuid

db = firestore.client()

class MaterialService:
    @staticmethod
    def add_material(topic_id: str, material: MaterialCreate, is_subtopic: bool = False, subtopic_id: str = None):
        """Adds a study material under a topic or subtopic."""
        material_id = str(uuid.uuid4())

        # Determine reference path (Topic or Subtopic)
        topic_ref = db.collection("topics").document(topic_id)
        if is_subtopic:
            topic_ref = topic_ref.collection("subtopics").document(subtopic_id)
        
        materials_ref = topic_ref.collection("materials").document(material_id)
        
        material_data = material.dict()
        material_data.update({
            "id": material_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

        materials_ref.set(material_data)
        return MaterialResponse(**material_data)

    @staticmethod
    def get_materials(topic_id: str, is_subtopic: bool = False, subtopic_id: str = None):
        """Fetches all study materials under a topic or subtopic."""
        topic_ref = db.collection("topics").document(topic_id)
        if is_subtopic:
            topic_ref = topic_ref.collection("subtopics").document(subtopic_id)

        materials = topic_ref.collection("materials").stream()
        return [material.to_dict() for material in materials]
