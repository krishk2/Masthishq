
import requests
import os

API_BASE = "http://localhost:8000/api/v1"

def test_person_enrollment():
    url = f"{API_BASE}/remember/person"
    filename = "dummy_person.jpg"
    
    # Create dummy image
    with open(filename, "wb") as f:
        f.write(os.urandom(1024))
        
    data = {"name": "Test Person", "relation": "Friend", "age": "30", "notes": "Integration test"}
    
    # Open, Send, Close
    with open(filename, "rb") as f_img:
        files = {"file": (filename, f_img, "image/jpeg")}
        response = requests.post(url, data=data, files=files)
    
    print(f"Person Enroll Response: {response.status_code} - {response.text}")
    
    if os.path.exists(filename):
        try: os.remove(filename)
        except: pass

    assert response.status_code == 200

def test_object_enrollment():
    url = f"{API_BASE}/remember/object"
    filename = "dummy_object.jpg"
    
    with open(filename, "wb") as f:
        f.write(os.urandom(1024))
        
    data = {"name": "Test Wallet", "notes": "My black wallet"}
    
    with open(filename, "rb") as f_img:
        files = {"file": (filename, f_img, "image/jpeg")}
        response = requests.post(url, data=data, files=files)
        
    print(f"Object Enroll Response: {response.status_code} - {response.text}")
    
    if os.path.exists(filename):
        try: os.remove(filename)
        except: pass

    assert response.status_code == 200

if __name__ == "__main__":
    print("Running Person Enrollment Test...")
    try:
        test_person_enrollment()
        print("✅ Person Enrollment Passed")
    except Exception as e:
        print(f"❌ Person Enrollment Failed: {e}")

    print("\nRunning Object Enrollment Test...")
    try:
        test_object_enrollment()
        print("✅ Object Enrollment Passed")
    except Exception as e:
        print(f"❌ Object Enrollment Failed: {e}")
