from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import os
import uuid
from pydub import AudioSegment
from pydub.silence import split_on_silence
from chatbot import get_chatbot_reply  # Student 3

app = Flask(__name__)

# ✅ Load faster-whisper once
whisper_model = WhisperModel("base", compute_type="int8")  # fast on CPU

# 🚨 Emergency keywords for alert detection
EMERGENCY_KEYWORDS = {"emergency", "help", "fire", "danger", "police", "accident"}

def check_emergency(text):
    words = set(text.lower().split())
    return any(word in words for word in EMERGENCY_KEYWORDS)

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]
    file_id = str(uuid.uuid4())

    raw_path = f"temp_{file_id}.wav"
    converted_path = f"converted_{file_id}.wav"
    trimmed_path = f"trimmed_{file_id}.wav"

    # Save uploaded audio
    audio_file.save(raw_path)

    try:
        # 🔄 Convert to 16kHz mono
        audio = AudioSegment.from_file(raw_path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(converted_path, format="wav")

        # ✂️ Trim silence
        audio = AudioSegment.from_file(converted_path)
        chunks = split_on_silence(
            audio,
            min_silence_len=300,
            silence_thresh=audio.dBFS - 14,
            keep_silence=100
        )

        if chunks:
            trimmed_audio = sum(chunks)
            trimmed_audio.export(trimmed_path, format="wav")
        else:
            trimmed_path = converted_path  # fallback if mostly silent

    except Exception as e:
        return jsonify({"error": f"Audio processing failed: {e}"}), 500

    # 🔤 Transcribe using faster-whisper
    try:
        segments, _ = whisper_model.transcribe(trimmed_path, language="en")
        text = " ".join(segment.text for segment in segments).strip()
    except Exception as e:
        return jsonify({"error": f"Whisper failed: {e}"}), 500

    # 🚨 Check for emergency
    is_emergency = check_emergency(text)

    # 💬 Get chatbot reply
    try:
        chatbot_reply = get_chatbot_reply(text)
    except Exception as e:
        chatbot_reply = "Sorry, chatbot failed to respond."

    # 🧹 Clean up temp files
    for f in [raw_path, converted_path, trimmed_path]:
        if os.path.exists(f):
            os.remove(f)

    return jsonify({
        "transcription": text,
        "emergency": is_emergency,
        "chatbot_reply": chatbot_reply
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
