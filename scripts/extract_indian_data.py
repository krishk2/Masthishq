print("INIT: Script starting...")
import os
import shutil
print("INIT: Importing datasets...")
import datasets
print("INIT: Imports done.")
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Convolve" / "photo" / "voxceleb_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_indian_celebs():
    print("🚀 Starting extraction of Indian Celebrities from VoxCeleb1...")
    
    # Load the custom builder script
    # We use "audio1" config because that's where nationality is available in metadata
    ds = datasets.load_dataset(
        "scripts/custom_voxceleb.py", 
        "audio1", 
        trust_remote_code=True,
        split="train" # Use 'train' (dev) partition
    )
    
    
    # LOCAL IMAGE SOURCE
    LOCAL_IMG_ROOT = PROJECT_ROOT / "HQ-VoxCeleb" / "HQ-VoxCeleb" / "vox1" / "origin_faces"
    
    # Get list of local celebrities
    if not LOCAL_IMG_ROOT.exists():
        print(f"❌ Error: Local image directory not found at {LOCAL_IMG_ROOT}")
        return

    local_celebs = {p.name for p in LOCAL_IMG_ROOT.iterdir() if p.is_dir()}
    
    # 🧪 TEST MODE: Take only 1 person (preferably starting with 'A' to match partaa)
    sorted_celebs = sorted(list(local_celebs))
    if sorted_celebs:
        target = sorted_celebs[0] # e.g. "A.J._Buckley"
        print(f"🧪 TEST MODE: Restricting to single celebrity: {target}")
        local_celebs = {target}
    
    print(f"📂 Found {len(local_celebs)} local celebrity folders (Filtered to 1).")

    # Filter for celebrities that exist locally
    # We match 'speaker_name' (e.g. 'A.J._Buckley') with the folder name
    filtered_celebs = ds.filter(lambda x: x.get("speaker_name", "") in local_celebs)
    
    print(f"📊 Found {len(filtered_celebs)} clips matching local folders.")
    
    # Group by speaker
    speakers = {}
    
    for item in filtered_celebs:
        s_id = item['speaker_id']
        s_name = item['speaker_name']
        if s_id not in speakers:
            speakers[s_id] = {
                "name": s_name,
                "gender": item['speaker_gender'],
                "clips": []
            }
        # Keep track of clips (limit to 5 per person)
        if len(speakers[s_id]["clips"]) < 5:
            speakers[s_id]["clips"].append(item['audio']['path'])

    print(f"👥 Found {len(speakers)} matched speakers.")

    # Save data
    for s_id, data in speakers.items():
        person_dir = OUTPUT_DIR / f"{data['name'].replace(' ', '_')}_{s_id}"
        person_dir.mkdir(exist_ok=True)
        
        # Save Metadata
        with open(person_dir / "metadata.json", "w") as f:
            f.write(str(data))
            
        # 1. Copy Audio Files (from Dataset Script)
        for i, clip_path in enumerate(data["clips"]):
            src = Path(clip_path)
            dest = person_dir / f"voice_sample_{i}.wav"
            try:
                shutil.copy2(src, dest)
                # print(f"   Saved audio {dest.name}")
            except Exception as e:
                print(f"   Error copying audio {src}: {e}")

        # 2. Copy Local Images (from HQ-VoxCeleb)
        # Structure is likely: origin_faces/id10001/1.jpg ...
        local_face_dir = LOCAL_IMG_ROOT / s_id
        if local_face_dir.exists():
            print(f"   📸 Found local images for {data['name']} ({s_id})")
            # Copy first 5 images
            found_imgs = list(local_face_dir.glob("*.jpg")) + list(local_face_dir.glob("*.png"))
            for i, img_path in enumerate(found_imgs[:5]):
                dest = person_dir / f"face_{i}{img_path.suffix}"
                shutil.copy2(img_path, dest)
        else:
            print(f"   ⚠️ No local images found for {data['name']} ({s_id}) at {local_face_dir}")

    print(f"✅ Extraction Complete. Data saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    extract_indian_celebs()
