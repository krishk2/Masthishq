
from ultralytics import YOLO
import numpy as np
from PIL import Image
import os
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.models import Model

# Global model instance (lazy load)
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("🧠 Loading MobileNetV2 for Objects...")
        base = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
        _embedding_model = Model(inputs=base.input, outputs=base.output)
    return _embedding_model

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        print(f"DEBUG: Loading YOLO model '{model_path}'...", flush=True)
        self.detector = YOLO(model_path)
        print("DEBUG: YOLO loaded.", flush=True)
    
    def detect_objects(self, image_path: str):
        """Returns YOLO detections."""
        results = self.detector(image_path)
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    "object": self.detector.names[int(box.cls[0])],
                    "confidence": float(box.conf[0]),
                    "box": box.xyxy[0].tolist()
                })
        return detections

    def generate_embedding(self, image_path: str):
        """Generates 1280-d embedding for the full image (or crop)."""
        model = get_embedding_model()
        
        # Load and preprocess
        img = keras_image.load_img(image_path, target_size=(224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        # Predict
        embedding = model.predict(x, verbose=0)
        return embedding[0].tolist() # List of floats

# Global instance
detector = ObjectDetector()
