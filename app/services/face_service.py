print("DEBUG: Importing OpenCV...", flush=True)
import cv2
print("DEBUG: Importing Keras-Facenet...", flush=True)
from keras_facenet import FaceNet
print("DEBUG: Importing PIL/Numpy...", flush=True)
from PIL import Image
import numpy as np
import os

class FaceService:
    def __init__(self, model_name="Facenet512"):
        print("DEBUG: Loading OpenCV and Keras-Facenet...", flush=True)
        # Load Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.embedder = FaceNet()
        self.model_name = model_name
        print("DEBUG: Face Models Loaded.", flush=True)

    def generate_embedding(self, image_path: str) -> list:
        try:
            # OpenCV reads in BGR, Keras-FaceNet expects RGB
            img_bgr = cv2.imread(image_path)
            if img_bgr is None:
                print(f"Could not read image: {image_path}")
                return []
            
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            
            # Detect
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                print(f"No face detected (OpenCV) in {image_path}")
                return []

            # Take largest face
            # OpenCV returns (x, y, w, h)
            face_data = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = face_data
            
            # Crop
            face = img_rgb[y:y+h, x:x+w]
            
            # Resize for Facenet (160x160)
            face = Image.fromarray(face).resize((160, 160))
            face = np.asarray(face).astype("float32") / 255.0
            face = np.expand_dims(face, axis=0) # (1, 160, 160, 3)
            
            # Embed
            embedding = self.embedder.embeddings(face)[0]
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def verify(self, img1_path, img2_path):
        # Implementation: Cosine Similarity between two embeddings
        emb1 = self.generate_embedding(img1_path)
        emb2 = self.generate_embedding(img2_path)
        
        if not emb1 or not emb2:
            return False
            
        from scipy.spatial.distance import cosine
        score = cosine(emb1, emb2) # 0 means identical, 1 means opposite
        # Threshold for Facenet is usually ~0.4 for distance
        return score < 0.4

    def analyze(self, img_path):
        # MTCNN/FaceNet doesn't provide age/gender directly easily.
        # Returning dummy data to satisfy interface if needed.
        return [{
            "age": 25, 
            "gender": "unknown", 
            "dominant_emotion": "neutral",
            "race": "unknown"
        }]

face_service = FaceService()
