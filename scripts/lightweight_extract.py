
import os
import requests
import shutil
import zipfile
import csv
from pathlib import Path

# CONFIG
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Convolve" / "photo" / "voxceleb_data"
LOCAL_IMG_ROOT = PROJECT_ROOT / "HQ-VoxCeleb" / "HQ-VoxCeleb" / "vox1" / "origin_faces"
TEMP_DIR = PROJECT_ROOT / "temp_download"

# Public HuggingFace Mirror (No Auth Required)
BASE_URL = "https://huggingface.co/datasets/ProgramComputer/voxceleb/resolve/main/vox1"
FILES = [
    "vox1_dev_wav_partaa",
    "vox1_dev_wav_partab",
    "vox1_dev_wav_partac",
    "vox1_dev_wav_partad"
]
META_URL = "https://mm.kaist.ac.kr/datasets/voxceleb/meta/vox1_meta.csv"

def extract_indian_data_local():
    print("🚀 Starting ROBUST LOCAL extraction...")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Download Metadata
    print("⬇️  Downloading Metadata...")
    meta_path = TEMP_DIR / "vox1_meta.csv"
    if not meta_path.exists():
        try:
             r = requests.get(META_URL, verify=False) # Bypass SSL if needed
             with open(meta_path, 'wb') as f:
                 f.write(r.content)
        except Exception as e:
            print(f"❌ Failed to download metadata: {e}")
            return
            
    # 2. Parse Metadata for Indian Celebs
    print("🔍 Filtering Metadata...")
    target_ids = set()
    id_to_name = {}
    
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # Columns: VoxCeleb1 ID, VGGFace1 ID, Gender, Nationality, Set
                nat = row.get("Nationality", "").lower()
                if nat in ["india", "indian"]:
                    vid = row.get("VoxCeleb1 ID")
                    name = row.get("VGGFace1 ID")
                    if vid:
                        target_ids.add(vid)
                        id_to_name[vid] = name
                        
        print(f"🇮🇳 Found {len(target_ids)} Indian celebrities.")
        # print(f"   Sample: {list(target_ids)[:5]}")
    except Exception as e:
        print(f"❌ Error parsing metadata: {e}")
        return

    # 3. Download All Parts
    print("⬇️  Downloading Dataset Parts (This handles the split zip)...")
    parts_paths = []
    
    for fname in FILES:
        fpath = TEMP_DIR / fname
        parts_paths.append(fpath)
        
        # Check if already exists/downloaded
        if fpath.exists() and fpath.stat().st_size > 1000000: # Simple size check > 1MB
             print(f"   ✅ {fname} already exists.")
             continue
             
        url = f"{BASE_URL}/{fname}"
        print(f"   ⬇️  Downloading {fname}...")
        try:
            with requests.get(url, stream=True, verify=False) as r:
                r.raise_for_status()
                with open(fpath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
        except Exception as e:
             print(f"❌ Failed to download {fname}: {e}")
             return

    # 4. Concatenate
    full_zip_path = TEMP_DIR / "full_vox1.zip"
    if not full_zip_path.exists():
        print("🔗 Concatenating parts into full zip...")
        with open(full_zip_path, 'wb') as outfile:
            for p in parts_paths:
                with open(p, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)
    else:
        print("✅ Full zip already exists.")

    # 5. Extract Matching Files
    print(f"📦 Extracting audio for {len(target_ids)} targets...")
    
    try:
        with zipfile.ZipFile(full_zip_path, 'r') as z:
            file_list = z.namelist()
            count = 0
            
            # Optimization: Pre-check available IDs in zip to avoid loop? 
            # No, just iterate once.
            
            for f in file_list:
                # Format: wav/id10001/1zn.../00001.wav
                parts = f.split('/')
                if len(parts) > 2:
                    s_id = parts[1]
                    if s_id in target_ids and f.endswith('.wav'):
                        name = id_to_name.get(s_id, s_id)
                        
                        # Output dir: Name_ID
                        p_dir = OUTPUT_DIR / f"{name}_{s_id}"
                        p_dir.mkdir(exist_ok=True)
                        
                        # Limit: 5 clips per person
                        existing = len(list(p_dir.glob("voice_sample_*.wav")))
                        if existing < 25:
                            # Extract
                            z.extract(f, TEMP_DIR)
                            src = TEMP_DIR / f
                            dest = p_dir / f"voice_sample_{existing}.wav"
                            
                            # Ensure parent exist
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(src), str(dest))
                            count += 1
                            
            print(f"✅ Extracted {count} total clips.")
            
            # 6. Copy Images (Optional Sync)
            print("📸 Syncing local images...")
            if LOCAL_IMG_ROOT.exists():
                for s_id, name in id_to_name.items():
                    # Local folder matches 'Name'
                    local_p_dir = LOCAL_IMG_ROOT / name
                    if local_p_dir.exists():
                         p_dir = OUTPUT_DIR / f"{name}_{s_id}"
                         if p_dir.exists():
                             # Copy images
                             params = list(local_p_dir.glob("*.jpg")) + list(local_p_dir.glob("*.png"))
                             for i, img in enumerate(params[:25]):
                                 shutil.copy2(img, p_dir / f"face_{i}{img.suffix}")
                                 
    except Exception as e:
        print(f"❌ Extraction error: {e}")
    
    print("✨ ALL DONE.")

if __name__ == "__main__":
    extract_indian_data_local()
