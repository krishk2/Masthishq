from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Person / Family Member Schema ---
class FamilyMember(BaseModel):
    person_id: str
    name: str
    relation: str
    face_photos: List[str] = []     # Paths to stored images
    voice_samples: List[str] = []   # Paths to stored audio
    notes: Optional[str] = None
    created_at: datetime = datetime.now()

class FamilyMemberCreate(BaseModel):
    name: str
    relation: str
    notes: Optional[str] = None

# --- Object Schema ---
class PersonalObject(BaseModel):
    object_id: str
    name: str
    category: str # e.g. "Medicine", "Personal"
    location_desc: str # e.g. "On the bedside table"
    image_path: str
    usage_instructions: Optional[str] = None

# --- Location Schema ---
class SafeLocation(BaseModel):
    location_id: str
    name: str # e.g. "Home", "Park"
    latitude: float
    longitude: float
    radius_meters: float = 100.0

# --- Enrollment Response ---
class EnrollmentResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
