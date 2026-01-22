
import os
import shutil
from pathlib import Path
import json
import csv

# CONFIG
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Convolve" / "photo" / "voxceleb_data"
LOCAL_IMG_ROOT = PROJECT_ROOT / "HQ-VoxCeleb" / "HQ-VoxCeleb" / "vox1" / "origin_faces"
META_PATH = PROJECT_ROOT / "temp_download" / "vox1_meta.csv"

def refined_ingest():
    print("🚀 Starting REFINED ingestion (Indian Only, Max 25)...")
    
    # 0. Clean previous
    if OUTPUT_DIR.exists():
        print("🧹 Cleaning output dir...")
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Parse Metadata for Indian Names
    indian_names = set()
    try:
        if META_PATH.exists():
            with open(META_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    if row.get("Nationality", "").lower() in ["india", "indian"]:
                        # VGGFace1 ID matches local folder names
                        name = row.get("VGGFace1 ID")
                        if name:
                            indian_names.add(name)
            print(f"🇮🇳 Found {len(indian_names)} Indian celebs in metadata.")
        else:
            print("⚠️ Metadata not found, cannot filter by nationality. Using generic first 25.")
    except Exception as e:
         print(f"⚠️ Error parsing metadata: {e}")

    # 2. Iterate and Copy
    if not LOCAL_IMG_ROOT.exists():
        print(f"❌ Critical: Local image root not found at {LOCAL_IMG_ROOT}")
        return

    count = 0
    # List all local folders
    all_local = sorted([p for p in LOCAL_IMG_ROOT.iterdir() if p.is_dir()])
    
    for cele_dir in all_local:
        if count >= 25:
            break
            
        name = cele_dir.name # e.g. "Aamir_Khan"
        
        # Filter: Must be in Indian list (if list exists)
        if indian_names and name not in indian_names:
            continue
            
        # Copy
        p_dir = OUTPUT_DIR / f"{name}_local"
        p_dir.mkdir(exist_ok=True)
        
        images = list(cele_dir.glob("*.jpg")) + list(cele_dir.glob("*.png"))
        copied = 0
        # Copy up to 5 faces per person
        for i, img in enumerate(images[:5]):
            shutil.copy2(img, p_dir / f"face_{i}{img.suffix}")
            copied += 1
            
        if copied > 0:
            meta = {
                "name": name.replace("_", " "),
                "relation": "Celebrity",
                "notes": "Indian Celebrity Sample"
            }
            with open(p_dir / "metadata.json", "w") as f:
                json.dump(meta, f)
            print(f"   ✅ [{count+1}/25] Ingested {name}")
            count += 1
            
    print(f"✨ Ingestion complete. Total: {count}")

if __name__ == "__main__":
    refined_ingest()
