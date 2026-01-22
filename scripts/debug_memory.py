import sys
import os
sys.path.append(os.getcwd())
from app.services.memory_service import memory_service

def debug_search():
    print("--- Debugging Qdrant Memory ---")
    
    # 1. List all names
    print("Fetching snippets...")
    try:
        res = memory_service.client.scroll(
            collection_name="faces",
            limit=50,
            with_payload=True,
            with_vectors=False
        )
        points = res[0]
        print(f"Total Points Found: {len(points)}")
        
        names = []
        for p in points:
            name = p.payload.get('name', 'Unknown')
            names.append(name)
            print(f" - Payload: {p.payload}")
            
        print("\n--- Testing Search ---")
        names = ["emraan", "amir", "test"] 
        for test_name in names:
            print(f"\n--- Checking '{test_name}' ---")
            matches = memory_service.search_by_text(test_name)
            if matches:
                p = matches[0]
                name = p.payload.get("name")
                audio = p.payload.get("audio_base64")
                image = p.payload.get("image_base64") # Check for image
                
                audio_len = len(audio) if audio else 0
                image_len = len(image) if image else 0
                
                print(f"Found: {name}")
                print(f"Audio Present: {bool(audio)} ({audio_len} chars)")
                print(f"Image Present: {bool(image)} ({image_len} chars)")
            else:
                print("Not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_search()
