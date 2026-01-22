
import os
import sys
from bing_image_downloader import downloader

# Categories to download
OBJECTS = [
    "medicine box", "wall clock", "mobile phone", "keys bunch", 
    "spectacles", "tv remote", "water bottle", "shoes", "wallet", "book"
]

BASE_DIR = r"c:\Users\Krish\Downloads\Convolve\MYNursingHome"

def download_images():
    # Install if missing: pip install bing-image-downloader
    for obj in OBJECTS:
        folder_name = obj.replace(" ", "_")
        print(f"Downloading images for: {obj} -> {folder_name}")
        
        try:
            downloader.download(
                obj, 
                limit=30,  
                output_dir=BASE_DIR, 
                adult_filter_off=True, 
                force_replace=False, 
                timeout=60, 
                verbose=True
            )
            # Rename folder if needed? 
            # downloader creates output_dir/query_string
            # We want output_dir/folder_name.
            # actually downloader makes a subfolder with the query string.
            
            src = os.path.join(BASE_DIR, obj)
            dst = os.path.join(BASE_DIR, folder_name)
            
            if src != dst and os.path.exists(src):
                if os.path.exists(dst):
                    # Move files
                    import shutil
                    for f in os.listdir(src):
                        shutil.move(os.path.join(src, f), os.path.join(dst, f))
                    os.rmdir(src)
                else:
                    os.rename(src, dst)
                    
        except Exception as e:
            print(f"Error downloading {obj}: {e}")

if __name__ == "__main__":
    download_images()
