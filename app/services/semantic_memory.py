
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from app.core.config import settings
import uuid

class SemanticMemoryService:
    def __init__(self):
        # Local model, small and fast
        print("DEBUG: Loading Sentence Transformer...", flush=True)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2') 
        
        if settings.QDRANT_MODE == "local":
            self.client = QdrantClient(path=settings.QDRANT_PATH)
        else:
            self.client = QdrantClient(
                url=settings.get_qdrant_url(),
                api_key=settings.QDRANT_API_KEY
            )
            
        self.collection_name = "text_knowledge"
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # all-MiniLM-L6-v2 outputs 384 dimensions
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        
        # Ensure Payload Index for filtering by name
        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="name",
                field_schema="keyword"
            )
        except Exception as e:
            # Index might already exist
            print(f"Index creation note: {e}")

    def learn_person(self, person_data: dict):
        """
        Converts person data into semantic text memories.
        """
        name = person_data.get("name")
        relation = person_data.get("relation")
        notes = person_data.get("notes", "")
        
        # Create meaningful sentences
        texts = [
            f"{name} is my {relation}.",
            f"Notes about {name}: {notes}"
        ]
        
        points = []
        for txt in texts:
            if not txt.strip(): continue
            embedding = self.encoder.encode(txt).tolist()
            
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": txt,
                    "name": name,
                    "relation": relation,
                    "type": "person_bio"
                }
            ))
            
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Learned {len(points)} semantic facts about {name}")

    def search_knowledge(self, query: str, context_name: str = None, limit=3):
        """
        Hybrid Search:
        1. Semantic Vector Search
        2. Optional Metadata Filter (if context_name provided)
        """
        embedding = self.encoder.encode(query).tolist()
        print(f"DEBUG: Executing query_points for '{query}'...")
        
        query_filter = None
        if context_name:
            # Narrow down to specific person if context is active
            query_filter = Filter(
                must=[
                    FieldCondition(key="name", match=MatchValue(value=context_name))
                ]
            )
            
        res = self.client.query_points(
            collection_name=self.collection_name,
            query=embedding,
            query_filter=query_filter,
            limit=limit
        )
        
        return [match.payload for match in res.points]

# Global Instance (Lazy load might be better to avoid startup lag, but simplified here)
semantic_memory = SemanticMemoryService()
