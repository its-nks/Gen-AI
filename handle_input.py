import requests
import os
import re
from TTS.api import TTS
from pydub import AudioSegment

# Set ffmpeg path for pydub
AudioSegment.converter = "ffmpeg"

# File paths
full_call_path = "/var/lib/asterisk/sounds/custom/full_call.wav"
input_path = "/var/lib/asterisk/sounds/custom/caller_input.wav"
output_wav = "/var/lib/asterisk/sounds/custom/generated_response.wav"
loop_decision_file = "/tmp/loop_status.txt"

# 🔔 Use your actual alarm sound (from Gen_AI-training)
alarm_path = "/mnt/c/Users/nkson/OneDrive/Documents/Desktop/Gen_AI-training/alarm_sound.wav"

# STT + chatbot API
url = "http://localhost:5000/transcribe"

print("🐍 Running handle_input.py...")

# ✅ Step 0: Extract 4s voice from full call
if os.path.exists(full_call_path):
    call = AudioSegment.from_file(full_call_path, format="wav")
    caller_voice = call[:4000]
    caller_voice = caller_voice.set_channels(1).set_frame_rate(16000)
    caller_voice.export(input_path, format="wav")
    print("🎤 Extracted caller_input.wav from full_call.wav")
else:
    print("❌ full_call.wav not found.")
    exit()

# ✅ Step 1: Check audio length
if os.path.getsize(input_path) < 5000:
    print("⚠️ Audio too short or silent. Skipping STT and chatbot.")
    reply_text = "Sorry, I didn't hear anything. Could you repeat?"
    transcribed_text = ""
    is_emergency = False
else:
    # ✅ Step 2: Transcribe + chatbot reply
    try:
        with open(input_path, "rb") as f:
            response = requests.post(url, files={"audio": f})
        data = response.json()
    except Exception as e:
        print(f"❌ API call failed: {e}")
        data = {}

    transcribed_text = data.get("transcription", "").strip()
    reply_text = data.get("chatbot_reply", "").strip()
    is_emergency = data.get("emergency", False)

    print(f"🗣 Transcribed: '{transcribed_text}'")
    print(f"💬 Reply: '{reply_text}'")
    print(f"🚨 Emergency? {is_emergency}")

# ✅ Step 3: Handle emergency or TTS
# ✅ Step 3: Emergency or TTS reply
# ✅ Step 3: Emergency or TTS reply
if is_emergency:
    try:
        alarm_source = "/mnt/c/Users/nkson/OneDrive/Documents/Desktop/Gen_AI-training/alarm_sound.wav"
        audio = AudioSegment.from_file(alarm_source, format="wav")
        audio = audio.set_channels(1).set_frame_rate(8000)
        audio.export(output_wav, format="wav")
        print("🚨 Custom emergency alarm used.")
    except Exception as e:
        print(f"❌ Emergency alarm error: {e}")
        reply_text = "Emergency detected. Please evacuate immediately."
        is_emergency = False  # fallback to TTS
    # Skip TTS completely
    reply_text = ""  # Prevent fallback TTS below
else:
    # Do TTS as usual
    if not reply_text or len(reply_text) < 5:
        reply_text = "Sorry, I didn't catch that. Can you say it again?"
        print("⚠️ Using fallback reply.")

    try:
        print("🔊 Generating TTS...")
        tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=False, gpu=False)
        tts.tts_to_file(text=reply_text, file_path="/tmp/tmp_response.wav")

        audio = AudioSegment.from_file("/tmp/tmp_response.wav", format="wav")
        audio = audio.set_channels(1).set_frame_rate(8000)
        audio.export(output_wav, format="wav")
        print("✅ TTS response saved to generated_response.wav")
    except Exception as e:
        print(f"❌ TTS error: {e}")

# ✅ Step 4: End-call keyword check
end_keywords = {"bye", "goodbye", "exit", "thank", "thanks"}
words = set(re.findall(r'\b\w+\b', transcribed_text.lower()))
is_end = any(word in words for word in end_keywords)
print(f"🔁 End detected? {is_end}")

# ✅ Step 5: Write loop_status.txt
try:
    with open(loop_decision_file, "w") as f:
        f.write("END" if is_end else "CONTINUE")
    print(f"📝 loop_status.txt = {'END' if is_end else 'CONTINUE'}")
except Exception as e:
    print(f"❌ Could not write loop_status.txt: {e}")
