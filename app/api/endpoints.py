
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from app.services.face_service import face_service
from app.services.object_service import detector as object_service
from app.services.memory_service import memory_service
from app.services.tts_service import tts_service
import shutil
from pathlib import Path
import uuid
from typing import Dict, Any
import base64
from PIL import Image
import io

router = APIRouter()

TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

# Ensure enrollment dir exists
ENROLL_DIR = Path("photo/enrolled")
ENROLL_DIR.mkdir(parents=True, exist_ok=True)

def encode_image_base64(image_path: str):
    """Resize and encode image to base64 for storage."""
    try:
        with Image.open(image_path) as img:
            # Resize to thumbnail to save space (e.g., 300px max)
            img.thumbnail((300, 300))
            buffered = io.BytesIO()
            img.convert("RGB").save(buffered, format="JPEG", quality=70)
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

@router.post("/recognize/person")
async def recognize_person(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Receive an image, detect faces, search Qdrant for identity.
    """
    # 1. Save temp file
    file_id = str(uuid.uuid4())
    ext = Path(file.filename).suffix
    temp_path = TEMP_DIR / f"{file_id}{ext}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Generate Embedding
        # Note: FaceService currently returns list of floats or empty list
        embedding = face_service.generate_embedding(str(temp_path))
        
        if not embedding:
            return {"status": "no_face_detected", "person": None}
            
        # 3. Search Memory
        matches = memory_service.search_face(embedding)
        
        if matches:
             best_match = matches[0]
             # Check threshold (Cosine Similarity > 0.4 implies match)
             if best_match.score > 0.4:
                 name = best_match.payload.get("name", "Unknown")
                 relation = best_match.payload.get("relation", "Unknown")
                 notes = best_match.payload.get("notes", "")
                 
                 # TTS Feedback
                 greeting = f"Hello {name}."
                 if notes:
                      greeting += f" {notes}"
                 elif relation != "Unknown":
                     greeting += f" You are a {relation}."
                 
                 # background_tasks.add_task(tts_service.speak, greeting)

                 return {
                     "status": "identified",
                     "person": {
                         "name": name,
                         "relation": relation,
                         "confidence": best_match.score,
                         "id": best_match.payload.get("person_id"),
                         "notes": notes,
                         "image": best_match.payload.get("image_base64", None),
                         "audio": best_match.payload.get("audio_base64", None)
                     }
                 }

        return {"status": "unknown", "person": None}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()

@router.post("/remember/person")
async def remember_person(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    relation: str = Form("Acquaintance"),
    notes: str = Form(None),
    age: int = Form(None),
    file: UploadFile = File(...),
    audio_file: UploadFile = File(None)
):
    """Enroll a new person with optional voice sample."""
    file_id = str(uuid.uuid4())
    filename = f"{name.replace(' ', '_')}_{file_id}.jpg"
    perm_path = ENROLL_DIR / filename
    
    # Audio Path
    audio_b64 = None
    if audio_file:
         audio_path = Path("audio/enrolled") / f"{name.replace(' ', '_')}_{file_id}.webm"
         audio_path.parent.mkdir(parents=True, exist_ok=True)
         try:
             with open(audio_path, "wb") as buffer:
                 shutil.copyfileobj(audio_file.file, buffer)
             
             # Encode for Cloud
             with open(audio_path, "rb") as f:
                 audio_b64 = base64.b64encode(f.read()).decode("utf-8")
         except Exception as e:
             print(f"Error saving audio: {e}")

    try:
        # Save Image locally as backup
        with open(perm_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Generate Embedding
        embedding = face_service.generate_embedding(str(perm_path))
        
        if not embedding:
            perm_path.unlink()
            return {"status": "error", "message": "No face detected in enrollment photo."}

        # Encode Image for Cloud Storage
        img_b64 = encode_image_base64(str(perm_path))
        
        # 4. Generate Avatar
        from app.services.avatar_service import avatar_service
        avatar_url = avatar_service.generate_avatar(str(perm_path))
            
        # Store in Qdrant
        metadata = {
            "name": name,
            "relation": relation,
            "age": age,
            "type": "person",
            "notes": notes or f"This is {name}, your {relation}.",
            "image_base64": img_b64,
            "avatar_url": avatar_url
        }
        if audio_b64:
            metadata["audio_base64"] = audio_b64 # Store voice sample in cloud!

        memory_service.store_face_memory(
            person_id=name.replace(" ", "_"),
            embedding=embedding,
            metadata=metadata
        )
        
        msg = f"I have enrolled {name}."
        
        return {"status": "stored", "name": name, "avatar_url": avatar_url}
        
    except Exception as e:
        if perm_path.exists():
             perm_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/remember/patient")
async def remember_patient(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    relation: str = Form("Acquaintance"),
    notes: str = Form(None),
    age: int = Form(None),
    file: UploadFile = File(...),
    audio_file: UploadFile = File(None)
):
    """Enroll a new PATIENT/Person via Caregiver (Stored in 'patients' collection)"""
    file_id = str(uuid.uuid4())
    filename = f"{name.replace(' ', '_')}_{file_id}.jpg"
    perm_path = ENROLL_DIR / filename
    
    # Audio Path
    audio_b64 = None
    if audio_file:
         audio_path = Path("audio/enrolled") / f"{name.replace(' ', '_')}_{file_id}.webm"
         audio_path.parent.mkdir(parents=True, exist_ok=True)
         try:
             with open(audio_path, "wb") as buffer:
                 shutil.copyfileobj(audio_file.file, buffer)
             with open(audio_path, "rb") as f:
                 audio_b64 = base64.b64encode(f.read()).decode("utf-8")
         except Exception as e:
             print(f"Error saving audio: {e}")

    try:
        # Save Image
        with open(perm_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Generate Embedding
        embedding = face_service.generate_embedding(str(perm_path))
        
        if not embedding:
            perm_path.unlink()
            return {"status": "error", "message": "No face detected in enrollment photo."}

        # Encode for storage
        img_b64 = encode_image_base64(str(perm_path))
        
        # Generate Avatar
        from app.services.avatar_service import avatar_service
        avatar_url = avatar_service.generate_avatar(str(perm_path))
            
        # Store in Qdrant PATIENTS collection
        metadata = {
            "name": name,
            "relation": relation,
            "age": age,
            "type": "patient_contact",
            "notes": notes or f"This is {name}, your {relation}.",
            "image_base64": img_b64,
            "avatar_url": avatar_url
        }
        if audio_b64:
            metadata["audio_base64"] = audio_b64

        memory_service.store_patient_memory(
            person_id=name.replace(" ", "_"),
            embedding=embedding,
            metadata=metadata
        )
        
        return {"status": "stored", "name": name, "avatar_url": avatar_url}
        
    except Exception as e:
        if perm_path.exists():
             perm_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/remember/object")
async def remember_object(
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    notes: str = Form(None),
    file: UploadFile = File(...)
):
    """Register a new personal object (e.g. Medicine Box)"""
    file_id = str(uuid.uuid4())
    temp_path = TEMP_DIR / f"{file_id}_{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Generate Embedding
        embedding = object_service.generate_embedding(str(temp_path))
        
        # Encode
        img_b64 = encode_image_base64(str(temp_path))

        # Store
        memory_service.store_object_memory(
            object_id=str(uuid.uuid4()),
            embedding=embedding,
            metadata={
                "name": name,
                "type": "object",
                "notes": notes or f"This is your {name}.",
                "image_base64": img_b64
            }
        )
        
        msg = f"I have remembered your {name}."
        # background_tasks.add_task(tts_service.speak, msg)
        
        return {"status": "stored", "name": name}
        
    finally:
        if temp_path.exists():
            temp_path.unlink()

@router.post("/find/object")
async def find_object(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Identify a specific personal object."""
    file_id = str(uuid.uuid4())
    temp_path = TEMP_DIR / f"{file_id}_{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Generate Embedding
        embedding = object_service.generate_embedding(str(temp_path))
        
        # 2. Search
        matches = memory_service.search_object(embedding)
        
        found_name = "Unknown Object"
        found_notes = ""
        found_img = None
        
        if matches and matches[0].score > 0.6: # Threshold
            best = matches[0]
            found_name = best.payload.get("name", "Unknown")
            found_notes = best.payload.get("notes", "")
            found_img = best.payload.get("image_base64", None)
            
            # TTS
            msg = f"This looks like your {found_name}."
            if found_notes:
                msg += f" {found_notes}"
            # background_tasks.add_task(tts_service.speak, msg)
            
            return {
                "status": "identified", 
                "object": {
                    "name": found_name, 
                    "notes": found_notes, 
                    "confidence": best.score,
                    "location": best.payload.get("location", "Unknown"),
                    "image": found_img
                }
            }
        
        # Fallback: YOLO Detection -> Auto-Enroll
        detections = object_service.detect_objects(str(temp_path))
        if detections:
            # Found "cell phone", "bottle", etc.
            # Pick the highest confidence object
            best_det = max(detections, key=lambda x: x['confidence'])
            label = best_det['object']
            
            # Auto-Learn: Store this specific instance embedding
            object_id = str(uuid.uuid4())
            # Use the already calculated embedding
            # Note: We should ideally crop the object, but full image embedding is OK for prototype 
            # if the object is dominant.
            
            # Encode for storage
            img_b64 = encode_image_base64(str(temp_path))
            
            # Determine location (Mock or Current Context)
            # Since we don't have GPS, we say "Last Seen Location" or date
            from datetime import datetime
            timestamp = datetime.now().strftime("%I:%M %p")
            location = f"Last seen at {timestamp}"

            memory_service.store_object_memory(
                object_id=object_id,
                embedding=embedding,
                metadata={
                    "name": label,
                    "type": "object",
                    "notes": "Auto-enrolled from observation.",
                    "location": location,
                    "image_base64": img_b64
                }
            )
            
            found_name = label
            found_notes = "I just learned this object."
            
            # Return as 'identified' so Frontend treats it as a known object
            return {
                "status": "identified", 
                "object": {
                    "name": found_name, 
                    "notes": found_notes, 
                    "confidence": best_det['confidence'],
                    "location": location,
                    "image": img_b64
                }
            }
            
        return {"status": "unknown", "object": None}
        
    finally:
        if temp_path.exists():
            temp_path.unlink()
@router.get("/debug/names")
async def debug_names():
    """List all names in Qdrant Faces"""
    try:
        res = memory_service.client.scroll(
            collection_name="faces",
            limit=100,
            with_payload=True
        )
        points = res[0]
        names = [p.payload.get("name") for p in points]
        return {"count": len(names), "names": names}
    except Exception as e:
        return {"error": str(e)}
