
from app.services.memory_service import memory_service
from app.services.semantic_memory import semantic_memory
import time

def migrate():
    print("--- Migrating existing memories to Vector Space ---")
    
    # 1. Fetch all faces
    res = memory_service.client.scroll(
        collection_name="faces",
        limit=1000,
        with_payload=True
    )
    points = res[0]
    print(f"Found {len(points)} existing face records.")
    
    for p in points:
        payload = p.payload
        if not payload: continue
        
        name = payload.get("name")
        if not name: continue
        
        print(f"Vectorizing {name}...")
        semantic_memory.learn_person(payload)
        
    print("--- Migration Complete ---")

if __name__ == "__main__":
    migrate()
