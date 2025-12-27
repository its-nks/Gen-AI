import torch
from TTS.api import TTS
import subprocess
import uuid
import os

# Allow RAdam for secure deserialization
from torch.serialization import add_safe_globals
from TTS.utils.radam import RAdam
from collections import defaultdict
add_safe_globals([RAdam, defaultdict, dict])  # Add dict now


# Create TTS instance with sweet female voice model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# Text input
text = "Hello! I am a calling bot . How can I assist you today?"

# Generate unique filename
file_id = str(uuid.uuid4())
wav_path = f"polite_reply.wav"
ulaw_path = f"polite_reply.ulaw"

# Generate TTS output
tts.tts_to_file(text=text, file_path=wav_path)

# Convert .wav to .ulaw using sox (must be installed)
try:
    subprocess.run([
        "sox", wav_path, "-r", "8000", "-c", "1", "-t", "ul", ulaw_path
    ], check=True)
    print(f"\n✅ Audio generated and converted to ULaw:\n→ {ulaw_path}")
except subprocess.CalledProcessError as e:
    print("❌ Error converting to .ulaw:", e)
