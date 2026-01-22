
from app.services.memory_service import memory_service

def reset_objects():
    print("🗑️ Deleting 'objects' collection...")
    try:
        memory_service.client.delete_collection("objects")
        print("✅ Deleted.")
    except Exception as e:
        print(f"⚠️ Error deleting: {e}")

    print("🆕 Recreating 'objects' collection with new config (1280d)...")
    memory_service._ensure_collections()
    print("✅ Done.")

if __name__ == "__main__":
    reset_objects()
