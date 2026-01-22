
from qdrant_client import QdrantClient

try:
    client = QdrantClient(path="qdrant_storage")
    print("✅ Client initialized.")
    attrs = dir(client)
    relevant = [a for a in attrs if "search" in a or "query" in a or "recommend" in a]
    print(f"Relevant methods: {relevant}")
except Exception as e:
    print(f"❌ Error: {e}")
