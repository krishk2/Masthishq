import requests
import os

# Configuration
API_URL = "http://localhost:8000/api/v1/remember/object"
IMAGE_PATH = r"C:\Users\Krish\.gemini\antigravity\brain\c4cf28c3-7dcb-4eb5-b929-90035746f34b\medicine_box_1768902160191.png"

def reenroll():
    if not os.path.exists(IMAGE_PATH):
        print(f"Image not found at {IMAGE_PATH}")
        return

    print(f"Re-enrolling Medicine Box from {IMAGE_PATH}...")
    
    with open(IMAGE_PATH, "rb") as f:
        files = {"file": ("medicine_box.png", f, "image/png")}
        data = {
            "name": "Medicine Box",
            "notes": "My daily pills. Keep on the kitchen table."
        }
        
        try:
            response = requests.post(API_URL, files=files, data=data)
            if response.status_code == 200:
                print("Success! Response:", response.json())
            else:
                print(f"Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Connection Error: {e}")

if __name__ == "__main__":
    reenroll()
