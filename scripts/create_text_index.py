
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "faces"

def create_indexes():
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Create Full Text Index on Name, Relation, Notes
    fields = ["name", "relation", "notes"]
    
    for field in fields:
        print(f"Creating Text Index for '{field}'...")
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=field,
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer=models.TokenizerType.WORD,
                min_token_len=2,
                max_token_len=15,
                lowercase=True
            )
        )

    print("✅ Indexes Created!")

if __name__ == "__main__":
    create_indexes()
