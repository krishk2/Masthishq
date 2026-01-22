
import sys
import os
sys.path.append(os.getcwd())
from qdrant_client import QdrantClient
from app.core.config import settings
import inspect

def test_qdrant():
    print("--- Inspecting Qdrant Client ---")
    if settings.QDRANT_MODE == "local":
        print(f"Mode: Local, Path: {settings.QDRANT_PATH}")
        client = QdrantClient(path=settings.QDRANT_PATH)
    else:
        print("Mode: Remote")
        client = QdrantClient(url=settings.get_qdrant_url(), api_key=settings.QDRANT_API_KEY)

    print(f"Client Type: {type(client)}")
    
    methods = [m for m in dir(client) if not m.startswith("_")]
    print(f"Methods: {methods}")
    
    print("\n--- Testing Search Methods ---")
    has_search = hasattr(client, 'search')
    has_query = hasattr(client, 'query_points')
    print(f"Has .search(): {has_search}")
    print(f"Has .query_points(): {has_query}")

    if has_search:
        print("Testing .search()...")
        try:
            # Dummy search
            client.search(collection_name="test", query_vector=[0.0]*384, limit=1)
        except Exception as e:
            print(f"Search Error: {e}")

if __name__ == "__main__":
    test_qdrant()
