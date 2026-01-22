
from qdrant_client import QdrantClient

try:
    client = QdrantClient(path="qdrant_storage")
    print("✅ Client initialized.")
    if client.get_collection("faces"):
        print("✅ Collection 'faces' exists.")
        
        # Test query_points
        try:
             # Dummy vector 512 dim
             dummy = [0.1] * 512
             res = client.query_points(collection_name="faces", query=dummy, limit=1)
             print(f"✅ query_points success. Result type: {type(res)}")
             print(f"Result: {res}")
        except Exception as e:
            print(f"❌ query_points failed: {e}")
            
except Exception as e:
    print(f"❌ Error: {e}")
