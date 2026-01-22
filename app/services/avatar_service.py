import requests
import os

READY_PLAYER_ME_API = "https://api.readyplayer.me/v1/avatars"

class AvatarService:
    def generate_avatar(self, image_path: str) -> str:
        """
        Generates a 3D avatar from a photo using Ready Player Me.
        Returns the URL of the generated avatar (GLB or PNG).
        """
        try:
            with open(image_path, "rb") as img:
                # RPM allows POSTing image to generate avatar
                response = requests.post(
                    READY_PLAYER_ME_API,
                    files={"file": img},
                    data={"gender": "neutral"}, # or detect gender? neutral is safe
                    headers={} # API Key optional for basic use
                )
            
            if response.status_code in [200, 201]:
                # Response format: {"data": {"id": "...", "url": "https://models.readyplayer.me/....glb", ...}}
                data = response.json().get("data", {})
                glb_url = data.get("url")
                
                # Convert GLB URL to PNG URL for 2D display
                # Standard RPM URL: https://models.readyplayer.me/<id>.glb
                # PNG Render: https://models.readyplayer.me/<id>.png
                if glb_url and ".glb" in glb_url:
                    return glb_url.replace(".glb", ".png")
                return glb_url
            else:
                print(f"RPM Error: {response.text}")
                return None
        except Exception as e:
            print(f"Avatar Generation Failed: {e}")
            return None

avatar_service = AvatarService()
