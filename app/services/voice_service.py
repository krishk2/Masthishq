import whisper

class VoiceService:
    def __init__(self, model_size="base"):
        # Load model on init (might be slow first time)
        print("DEBUG: Loading Whisper model... (This may take time)", flush=True)
        self.model = whisper.load_model(model_size)
        print("DEBUG: Whisper model loaded.", flush=True)

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text.
        """
        try:
            result = self.model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return ""

    # Future: Speaker Identification using PyAnnote or similar matches?
    # For now, we focus on STT as requested in Milestone 3 "Speech processing using Whisper"
    
voice_service = VoiceService()
