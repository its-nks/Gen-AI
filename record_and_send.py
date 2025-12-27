import sounddevice as sd
from scipy.io.wavfile import write
import requests
import os

FILENAME = "live_audio.wav"
DURATION = 5  # seconds
FS = 16000  # Sample rate (Whisper prefers 16000 Hz)

def record_voice():
    print(f"🎙️ Recording for {DURATION} seconds...")
    audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='int16')
    sd.wait()
    write(FILENAME, FS, audio)
    print("✅ Recording saved as:", FILENAME)

def send_to_server():
    print("📤 Sending to /transcribe...")
    url = "http://localhost:5002/transcribe"
    with open(FILENAME, "rb") as f:
        files = {"audio": f}
        response = requests.post(url, files=files)
        print("✅ Response:")
        print(response.json())

if __name__ == "__main__":
    record_voice()
    send_to_server()
