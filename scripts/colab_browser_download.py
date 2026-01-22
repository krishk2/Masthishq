
# 📥 Run this cell in Google Colab to download the file to your local machine

from google.colab import files
import os

FILE_PATH = "/content/indian_celebs_audio.zip"

if os.path.exists(FILE_PATH):
    print(f"✅ Found file: {FILE_PATH}")
    print("⬇️ Starting download...")
    files.download(FILE_PATH)
else:
    print(f"❌ File not found at {FILE_PATH}. Did the previous step finish?")
