
import json
from pathlib import Path

BASE_DIR = Path("Convolve/photo/voxceleb_data")

# "Caregiver" style descriptions for the 26 celebs
DESCRIPTIONS = {
    "A._R._Rahman": "He is your favorite musician. You love listening to 'Jai Ho' in the mornings with tea.",
    "Aamir_Khan": "This is Aamir. You watched 'Lagaan' with him in the theater years ago. He visits occasionally.",
    "Abhishek_Bachchan": "This is Abhishek, Amitabh's son. You remember him from the tall family next door.",
    "Aishwarya_Rai_Bachchan": "Aishwarya, the beautiful actress. You always admired her elegance.",
    "Ajay_Devgn": "Ajay, the serious police officer from that movie you like. He is very reliable.",
    "Akshay_Kumar": "Akshay, the funny man from the comedy shows. He always makes you laugh.",
    "Amitabh_Bachchan": "Amitabh, the 'Big B'. You have his poster in your room. A legend.",
    "Anushka_Sharma": "Anushka, the bubbly girl. Reminds you of your granddaughter.",
    "Deepika_Padukone": "Deepika, the tall dancer. You sat next to her at the wedding reception.",
    "Emraan_Hashmi": "Emraan, the actor. You recognize him from the songs on the radio.",
    "Farhan_Akhtar": "Farhan, the singer. He reminds you of your college days.",
    "Freida_Pinto": "Freida, she lives abroad now but visits when she can.",
    "Hrithik_Roshan": "Hrithik, the dancer. You actully met him once at a gym.",
    "Irrfan_Khan": "Irrfan, such a soulful actor. You miss his movies.",
    "John_Abraham": "John, the strong boy from the gym. He helps carry heavy things.",
    "Kangana_Ranaut": "Kangana, the fierce lady. She speaks her mind, just like you.",
    "Kareena_Kapoor": "Kareena, the fashion icon. You liked her saree at the last function.",
    "Katrina_Kaif": "Katrina, the gentle girl. She brings you flowers.",
    "Mallika_Sherawat": "Mallika, the celebrity from the magazines.",
    "Naseeruddin_Shah": "Naseeruddin, the wise man. You enjoy his poetry readings.",
    "Om_Puri": "Om Puri, with the deep voice. A grand personality.",
    "Parineeti_Chopra": "Parineeti, Priyanka's cousin. A cheerful presence.",
    "Pooja_Kumar": "Pooja, a friend from the south. She cooks great Idli.",
    "Preity_Zinta": "Preity, the dimpled girl. She used to own that cricket team you watch.",
    "Priyanka_Chopra_Jonas": "Priyanka, she is famous in America now! Our local pride.",
    "Ranbir_Kapoor": "Ranbir, the Kapoor boy. Very charming.",
    "Randeep_Hooda": "Randeep, the rugged actor.",
    "Shah_Rukh_Khan": "Shah Rukh! The King itself. Your absolute favorite. You never miss his films.",
    "Shahid_Kapoor": "Shahid, the dancer boy.",
    "Shraddha_Kapoor": "Shraddha, the singer girl next door acts in movies."
}

def enrich_metadata():
    if not BASE_DIR.exists():
        print("❌ Dataset dir not found!")
        return

    count = 0
    for folder in BASE_DIR.iterdir():
        if folder.is_dir():
            name = folder.name
            meta_path = folder / "metadata.json"
            
            # Default metadata if missing
            data = {"name": name.replace("_", " "), "relation": "Acquaintance"}
            
            if meta_path.exists():
                with open(meta_path, "r") as f:
                    try:
                        data = json.load(f)
                    except: pass
            
            # Enrich
            if name in DESCRIPTIONS:
                data["notes"] = DESCRIPTIONS[name] # Use 'notes' for the description
                data["summary"] = DESCRIPTIONS[name] 
                # Also relation update slightly?
                if "Bachchan" in name:
                     data["relation"] = "Family Friend"
                elif "Khan" in name:
                     data["relation"] = "Close Friend"
            
            with open(meta_path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Enriched {name}")
            count += 1

    print(f"✨ Updated {count} profiles with Amnesia-friendly notes.")

if __name__ == "__main__":
    enrich_metadata()
