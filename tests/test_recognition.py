
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# Ensure app is importable
sys.path.insert(0, os.getcwd())

from app.main import app

client = TestClient(app)
DATA_DIR = Path("Convolve/photo/voxceleb_data")

def test_recognition():
    print("🧪 Starting Recognition Test...")
    
    # 1. Inspect Data
    if not DATA_DIR.exists():
        print(f"❌ Data dir not found: {DATA_DIR}")
        return

    # Find Aamir Khan (known Indian celeb)
    target_dir = next(DATA_DIR.glob("*Aamir_Khan*"), None)
    if not target_dir:
        print("⚠️ Aamir Khan not found. Picking any available person...")
        target_dir = next(DATA_DIR.glob("*_local"), None)
        
    if not target_dir:
        print("❌ No data found in voxceleb_data!")
        return
        
    print(f"🎯 Target Person: {target_dir.name}")
    
    # Pick an image
    img_path = next(target_dir.glob("*.jpg"), next(target_dir.glob("*.png"), None))
    if not img_path:
        print("❌ No images found for target.")
        return
        
    print(f"📸 Testing with image: {img_path}")
    
    # 2. Call API
    try:
        with open(img_path, "rb") as f:
            response = client.post(
                "/api/v1/recognize/person",
                files={"file": ("test.jpg", f, "image/jpeg")}
            )
            
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        
        # 3. Verify
        data = response.json()
        if response.status_code == 200 and data.get("status") == "identified":
            name = data["person"]["name"]
            conf = data["person"]["confidence"]
            print(f"✅ SUCCESS! Identified as: {name} (Conf: {conf:.2f})")
        else:
            print("❌ FAILURE. Not identified.")
            
    except Exception as e:
        print(f"💥 Exception during test: {e}")

if __name__ == "__main__":
    test_recognition()
