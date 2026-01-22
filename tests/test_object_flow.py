
from fastapi.testclient import TestClient
from app.main import app
import os

# Use the generated artifact path
IMG_PATH = r"C:\Users\Krish\.gemini\antigravity\brain\c4cf28c3-7dcb-4eb5-b929-90035746f34b\medicine_box_1768902160191.png"

client = TestClient(app)

def test_object_flow():
    if not os.path.exists(IMG_PATH):
        print(f"Image not found at {IMG_PATH}")
        return

    print("Testing Object Memory Flow...")

    # 1. REMEMBER
    print("\n[1] Registering Object: Heart Medicine...")
    with open(IMG_PATH, "rb") as f:
        # TestClient uses 'files' differently? No, same requests API.
        files = {"file": ("medicine.png", f, "image/png")}
        data = {
            "name": "Heart Medicine", 
            "notes": "Take two pills after dinner."
        }
        res = client.post("/api/v1/remember/object", files=files, data=data)
    
    if res.status_code == 200:
        print(f"Stored: {res.json()}")
    else:
        print(f"Failed to store: {res.text}")
        return

    # 2. FIND
    print("\n[2] Finding Object (Same Image)...")
    with open(IMG_PATH, "rb") as f:
        files = {"file": ("query.png", f, "image/png")}
        res = client.post("/api/v1/find/object", files=files)
        
    print(f"Code: {res.status_code}")
    print(f"Response: {res.json()}")
    
    if res.status_code == 200 and res.json().get("status") == "identified":
        print("SUCCESS! Object Identified.")
    else:
        print("Failed or Low Confidence.")

if __name__ == "__main__":
    test_object_flow()
