
import sys
import os
sys.path.append(os.getcwd())
from app.services.memory_service import memory_service
from app.core.config import settings

def check_cloud():
    print(f"--- Qdrant Cloud Debug ---")
    print(f"URL: {settings.QDRANT_URL}")
    print(f"Mode: {settings.QDRANT_MODE}")
    
    try:
        colls = memory_service.client.get_collections()
        print(f"Collections: {[c.name for c in colls.collections]}")
        
        if "faces" in [c.name for c in colls.collections]:
            count = memory_service.client.count("faces")
            print(f"Count 'faces': {count.count}")
            
            if count.count > 0:
                print("Retrieving one point...")
                res = memory_service.search_face([0.1]*512, limit=1) # Dummy vector
                if res:
                    print(f"Sample Payload Keys: {list(res[0].payload.keys())}")
                    if "image_base64" in res[0].payload:
                        print("✅ image_base64 is present!")
                    else:
                        print("❌ image_base64 missing!")
        else:
            print("❌ 'faces' collection not found!")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    check_cloud()
