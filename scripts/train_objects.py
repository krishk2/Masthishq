
import os
import sys
import uuid

# Fix path
sys.path.append(os.getcwd())

from app.services.memory_service import memory_service
from app.services.object_service import detector
from tqdm import tqdm

BASE_DIR = r"c:\Users\Krish\Downloads\Convolve\MYNursingHome"

LOCATION_MAP = {
    "bed": "Bedroom 101",
    "chair": "Common Area",
    "medicine_box": "Nurse Station",
    "keys": "Reception Desk",
    "wheelchair": "Entrance Lobby",
    "walker": "Corridor A",
    "clock": "Wall (Hallway)",
    "phone": "Living Room",
    "spectacles": "Bedside Table",
    "remote": "TV Room",
    "water_bottle": "Kitchen",
    "shoes": "Shoe Rack",
    "wallet": "Safe Box",
    "book": "Library Shelf",
    "basket_bin": "Corner",
    "bench": "Garden",
    "cabinet": "Storage Room",
    "call_bell": "Bedside",
    "cane_stick": "Entrance",
    "door": "Main Entrance",
    "electric_socket": "Wall",
    "fan": "Ceiling",
    "fire_extinguisher": "Hallway B",
    "handrail": "Stairs",
    "human_being": "Everywhere",
    "rack": "Store",
    "refrigerator": "Kitchen",
    "shower": "Bathroom",
    "sink": "Washroom",
    "sofa": "Lounge",
    "table": "Dining Hall",
    "television": "TV Room",
    "toilet_seat": "Restroom",
    "wardrobe": "Bedroom 101",
    "water_dispencer": "Corridor B"
}

def train_objects():
    print("--- Training Object Memory ---")
    
    # Iterate Categories
    if not os.path.exists(BASE_DIR):
        print(f"Directory not found: {BASE_DIR}")
        return

    categories = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    
    total_stored = 0
    
    for cat in tqdm(categories, desc="Categories"):
        cat_path = os.path.join(BASE_DIR, cat)
        location = LOCATION_MAP.get(cat.lower(), "General Storage")
        
        # Iterate Images
        images = [f for f in os.listdir(cat_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Limit to 5 images per category to save time/space for prototype
        # Or do all? Let's do 10.
        for img_name in images[:10]:
            img_path = os.path.join(cat_path, img_name)
            
            try:
                # Generate Embedding
                embedding = detector.generate_embedding(img_path)
                
                # Store
                metadata = {
                    "name": cat,
                    "type": "object", 
                    "location": location,
                    "filename": img_name
                }
                
                memory_service.store_object_memory(
                    object_id=str(uuid.uuid4()),
                    embedding=embedding,
                    metadata=metadata
                )
                total_stored += 1
                
            except Exception as e:
                print(f"Error processing {img_name}: {e}")
                
    print(f"--- Training Complete. Stored {total_stored} objects. ---")

if __name__ == "__main__":
    train_objects()
