import whisper
import os

# Upgrade to "small" model for better accuracy (or use "medium" for best results)
# Note: Larger models need more RAM but give better transcription
model = whisper.load_model("small")

def transcribe_audio(file_path: str) -> str:
    # Use fp16=False for CPU to avoid precision issues
    result = model.transcribe(file_path, fp16=False)
    return result["text"]
