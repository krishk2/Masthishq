
import os
import shutil
import json
import random
from pathlib import Path

# Paths
BASE_DIR = Path("Convolve/photo/voxceleb_data")
AUDIO_SRC_DIR = BASE_DIR / "indian_celebs_audio (1)"
FACES_SRC_DIR = BASE_DIR # The _local folders are directly in BASE_DIR

# Rich Metadata Generators
RELATIONS = ["Friend", "Colleague", "Mentor", "Acquaintance", "Family", "Rival", "Partner"]
MEMORIES = [
    "Met at a tech conference in Mumbai.",
    "Collaborated on a creative project in 2024.",
    "Shared a coffee and discussed future of AI.",
    "Went to the same university.",
    "Worked together on a film set.",
    "Met during a charity event.",
    "Regular tennis partner on weekends.",
    "Discussed philosophy during a long flight.",
    "Childhood neighbor from Delhi."
]

def normalize_name(folder_name):
    # Removes _local, _idXXXX
    name = folder_name.replace("_local", "")
    if "_id" in name:
        name = name.split("_id")[0]
    return name

def merge_data():
    print("🚀 Starting Data Merge & Enrichment...")
    
    # Track all unique persons
    persons = set()
    
    # 1. Scan Face Folders
    face_folders = [f for f in FACES_SRC_DIR.iterdir() if f.is_dir() and "_local" in f.name]
    for f in face_folders:
        persons.add(normalize_name(f.name))
        
    # 2. Scan Audio Folders
    if AUDIO_SRC_DIR.exists():
        audio_folders = [f for f in AUDIO_SRC_DIR.iterdir() if f.is_dir()]
        for f in audio_folders:
            persons.add(normalize_name(f.name))
    else:
        print("⚠️ Audio directory not found!")
        audio_folders = []

    print(f"👥 Found {len(persons)} unique persons.")

    # 3. Create Unified Folders
    for p_name in persons:
        target_dir = BASE_DIR / p_name
        target_dir.mkdir(exist_ok=True)
        print(f"Processing {p_name}...")
        
        # Merge Face Data
        face_src = BASE_DIR / f"{p_name}_local"
        if face_src.exists():
            for item in face_src.iterdir():
                if item.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    shutil.copy2(item, target_dir / item.name)
            # Remove old folder? Or keep backup? User said "proceed now", implies robust structure.
            # I'll keep old for safety for now, or delete if name collision isn't issue.
            # Actually, renaming might be cleaner?
            # copy is safer.

        # Merge Audio Data
        # Audio folder name might be p_name + "_idXXXX"
        # Find matching folder in AUDIO_SRC_DIR
        matching_audio = [f for f in audio_folders if normalize_name(f.name) == p_name]
        if matching_audio:
            a_src = matching_audio[0] # Take first match
            for item in a_src.iterdir():
                if item.suffix.lower() == '.wav':
                    shutil.copy2(item, target_dir / item.name)

        # Generate Rich Metadata
        metadata = {
            "name": p_name.replace("_", " "),
            "id": p_name, # Simple ID
            "relation": random.choice(RELATIONS),
            "summary": random.choice(MEMORIES),
            "context": {
                "last_seen": "2025-12-01",
                "notes": f"Generated profile for {p_name}"
            }
        }
        
        # Save Metadata
        with open(target_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)
            
    print("✨ Merge Complete. Data structured.")

if __name__ == "__main__":
    merge_data()
