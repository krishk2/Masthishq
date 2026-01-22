
import sys
import os
import json
import shutil
from pathlib import Path
import base64
from PIL import Image
import io

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.schemas import FamilyMember, PersonalObject
from app.services.face_service import face_service
from app.services.object_service import detector as object_service
from app.services.memory_service import memory_service

# CONFIG
SOURCE_DIR = Path("Convolve/photo")
DATASET_DIR = SOURCE_DIR / "voxceleb_data"
AUDIO_DIR = SOURCE_DIR / "audio"
OBJECTS_DIR = SOURCE_DIR / "objects"

# MOCK METADATA
METADATA = {
    "person_01": {
        "name": "Swarnanjali",
        "relation": "College Friend",
        "notes": "Your closest friend from college days."
    },
    "spectacles": {
        "name": "Spectacles",
        "category": "Personal",
        "location": "Bedside table",
        "usage": "Used for reading"
    }
}

def encode_image(path):
    try:
        with Image.open(path) as img:
            img.thumbnail((300, 300))
            buffered = io.BytesIO()
            img.convert("RGB").save(buffered, format="JPEG", quality=70)
            return f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"
    except: return None

def encode_audio(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except: return None

def seed_data():
    print("🌱 Starting Data Seed...")
    
    # 0. RESET COLLECTIONS
    try:
        memory_service.client.delete_collection("faces")
        print("🗑️ Deleted old 'faces' collection (Clean Slate).")
    except Exception as e:
        print(f"⚠️ Could not delete faces collection (might not exist): {e}")

    memory_service._ensure_collections()
    print("✨ Collections ready.")
    
    # 1. PERSONS
    persons = []
    if DATASET_DIR.exists():
        for person_dir in DATASET_DIR.iterdir():
            if person_dir.is_dir():
                pid = person_dir.name
                meta = {"name": f"Unknown ({pid})", "relation": "Unknown"}
                
                # Dynamic Metadata
                if (person_dir / "metadata.json").exists():
                    try:
                        with open(person_dir / "metadata.json") as f:
                            meta.update(json.load(f))
                    except: pass
                elif pid in METADATA:
                     meta.update(METADATA[pid])

                # Gather photos
                photos = [str(p) for p in person_dir.glob("*") if p.suffix.lower() in ['.jpg', '.jpeg', '.png']]
                
                # Gather voice
                voice_samples = [str(p) for p in person_dir.glob("*.wav")]
                if pid == "person_01" and (AUDIO_DIR / "swarnanjali_voice.wav").exists():
                     voice_samples.append(str(AUDIO_DIR / "swarnanjali_voice.wav"))

                person = FamilyMember(
                    person_id=pid,
                    name=meta["name"],
                    relation=meta["relation"],
                    face_photos=photos,
                    voice_samples=voice_samples,
                    notes=meta.get("notes")
                )
                persons.append(person)
                print(f"   👤 Found Person: {person.name} ({len(photos)} photos)")

    # 2. OBJECTS
    objects = []
    if OBJECTS_DIR.exists():
        for obj_file in OBJECTS_DIR.glob("*"):
            if obj_file.suffix.lower() in ['.png', '.jpg']:
                obj_id = obj_file.stem # e.g. "spectacles"
                meta = METADATA.get(obj_id, {"name": obj_id, "category": "Object", "location": "Unknown"})
                
                obj = PersonalObject(
                    object_id=obj_id,
                    name=meta["name"],
                    category=meta["category"],
                    location_desc=meta.get("location", ""),
                    image_path=str(obj_file),
                    usage_instructions=meta.get("usage")
                )
                objects.append(obj)
                print(f"   👓 Found Object: {obj.name}")

    # 3. PROCESSING
    print(f"\n🧠 Ingesting {len(persons)} Persons...")
    for p in persons:
        print(f"   Processing {p.name}...")
        for photo_path in p.face_photos:
            emb = face_service.generate_embedding(photo_path)
            if emb:
                img_b64 = encode_image(photo_path)
                
                # Encode first voice sample
                audio_b64 = None
                if p.voice_samples:
                     audio_b64 = encode_audio(p.voice_samples[0])

                metadata={
                    "name": p.name,
                    "relation": p.relation,
                    "notes": p.notes,
                    "image": str(photo_path),
                    "image_base64": img_b64
                }
                if audio_b64:
                    metadata["audio_base64"] = audio_b64

                memory_service.store_face_memory(
                    person_id=p.person_id,
                    embedding=emb,
                    metadata=metadata
                )
                print(f"     + Stored face vector")
            else:
                 print(f"     ! Failed to generate embedding for {photo_path}")

    # Process Objects
    print(f"\n🧠 Ingesting {len(objects)} Objects...")
    for obj in objects:
        print(f"   Processing {obj.name}...")
        emb = object_service.generate_embedding(obj.image_path) 
        if emb:
             img_b64 = encode_image(obj.image_path)
             memory_service.store_object_memory(
                object_id=obj.object_id,
                embedding=emb,
                metadata={
                    "name": obj.name,
                    "location": obj.location_desc,
                    "usage": obj.usage_instructions,
                    "category": obj.category,
                    "image_base64": img_b64
                }
             )
             print(f"     + Stored object vector for {obj.name}")

    print(f"\n✅ Seed Complete.")
    return persons, objects

if __name__ == "__main__":
    seed_data()
