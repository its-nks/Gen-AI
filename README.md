Calee AI – Intelligent Voice Call Assistant
Calee AI is an advanced AI-powered voice call assistant designed for real-time voice interactions. Built with Python, Asterisk PBX for call handling, and compatible SIP clients like Zoiper, Whisper-based speech recognition, and AI-driven response generation, Calee AI can converse with users, detect emergency situations, and respond via natural-sounding TTS (Text-to-Speech). It is ideal for automated customer support, voice-enabled bots, and intelligent communication systems.

🌟 Features

•	Real-time STT & TTS: Transcribe caller audio and generate instant voice responses.

•	Emergency Detection: Detect keywords like "help" and play a custom alarm audio (alarm_sound.wav).

•	End-Call Detection: Automatically hang up on keywords like "bye".

•	Asterisk Integration: Handles incoming calls, audio playback, and call management using dialplans and AGI scripts.

•	Modular Python Scripts: Clean separation of STT, TTS, chatbot, and call handling logic.

•	Audio Processing Utilities: Includes .wav → .ulaw conversion and playback support.

•	Configurable: Environment variables managed via .env for easy configuration.

•	SIP Client Compatible: Tested with Zoiper, but compatible with other SIP clients like Linphone or MicroSIP.

📁 Project Structure
callee_ai/
├── venv/                      # Python virtual environment
├── .env                       # Environment configuration
├── .gitignore                 # Git ignore rules
├── alarm_sound.wav            # Custom emergency alarm audio
├── deep_beep_ulaw.wav         # TTS/audio testing file
├── app.py                     # Main application entry point
├── chatbot.py                 # Chatbot logic for generating responses
├── handle_input.py            # Core voice input processing, STT/TTS loop, emergency/end-call handling
├── record_and_send.py         # Audio recording and file conversion utilities
├── stt.py                     # Speech-to-text logic
├── tts_test_script.py         # Test script for TTS generation
└── README.md                  # Project documentation

🚀 Getting Started
1. Clone the repository
•	git clone https://github.com/yourusername/callee_ai.git
•	cd callee_ai

2. Set up the Python environment
•	python -m venv venv
# Activate the virtual environment
•	source venv/bin/activate   # Linux/macOS
•	venv\Scripts\activate      # Windows
•	pip install -r requirements.txt

3.Configure environment variables
•	Copy or create a .env file with API keys, model parameters, and other necessary configurations.

📘 Usage

Start main application:
python app.py
TTS testing:
python tts_test_script.py
Record and send audio for processing:
python record_and_send.py

Call handling loop:
handle_input.py manages the real-time conversation, integrates STT, chatbot responses, TTS audio output, emergency detection, and automatic call hangup on end-call keywords.

🔑 Key Components
1. STT (stt.py)
•	Converts caller audio into text using Whisper or other STT engines.

2. TTS (tts_test_script.py)
•	Converts chatbot text responses into audio for playback.
•	Supports .wav and .ulaw formats for Asterisk.

3. Chatbot (chatbot.py)
•	Generates intelligent, context-aware responses based on transcribed text.

4. Call Handling (handle_input.py)
•	Main conversation loop integrating:
•	STT transcription
•	Chatbot response generation
•	TTS audio playback
•	Emergency detection → Plays alarm_sound.wav when keywords are detected
•	End-call detection → Hangs up the call automatically on keywords like "bye"

5. Audio Utilities (record_and_send.py)
•	Records caller audio, trims/adjusts duration, and converts to .ulaw for Asterisk playback.

6. Asterisk Integration
•	Handles incoming calls via dialplans (extensions.conf) using Record() or AGI scripts.
•	Plays TTS or custom audio (.ulaw) to callers.
•	Works with SIP clients like Zoiper, Linphone, or MicroSIP for testing and real call scenarios.

🛠️ Development Notes

•	Keep logic modular for easier debugging and extensions.
•	Audio caching can improve performance for repeated responses.
•	Emergency and end-call handling are critical: ensure the keywords are accurate and alarm audio is accessible.
•	Real-time response requires monitoring STT/TTS latency to maintain smooth conversation.
•	The project can run on Windows or WSL2/Linux, but Asterisk requires a Linux environment (WSL2 or server) to function properly.

🔧 Recommended Tools

•	Zoiper – SIP client for testing calls
•	Linphone – Alternative SIP softphone
•	MicroSIP – Lightweight Windows SIP client
