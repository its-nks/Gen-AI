Calee AI – Intelligent Voice Call Assistant

Calee AI is an advanced AI-powered voice call assistant designed to enable real-time voice interactions. Built with Python, Asterisk, Whisper-based speech recognition, and AI-driven response generation, Calee AI can converse with users, detect emergency situations, and respond via natural-sounding TTS (Text-to-Speech). It is ideal for automated customer support, voice-enabled bots, and intelligent communication systems.

Table of Contents

Features

Architecture

Technologies Used

Installation

Configuration

Usage

Folder Structure

Contributing

License

Features

Real-time Voice Conversation: Engages users instantly through speech recognition and AI-generated responses.

Emergency Detection: Detects specific emergency keywords (e.g., “help”, “fire”) and plays a custom alarm.

Call Termination: Automatically ends calls when end keywords (e.g., “bye”) are detected.

AI-Powered Responses: Uses GPT-based models to generate intelligent and context-aware replies.

Custom TTS Voices: Converts AI responses into natural-sounding voice messages.

Full Call Recording: Stores entire conversations for auditing or training purposes.

Integration with Asterisk: Seamlessly interacts with the Asterisk PBX system via AGI scripts or shell commands.

Architecture

Calee AI consists of the following modules:

Student 1 (Voice Bot Loop):

Captures user voice input.

Sends audio for STT (Speech-to-Text) processing.

Generates AI-based responses and TTS audio.

Plays response back to the caller.

Student 2 (STT & Emergency Detection):

Transcribes caller speech using Whisper / faster-whisper.

Detects emergency keywords and triggers alarms.

Backend & Asterisk Integration:

Handles call flow logic, looping, end-call detection, and audio playback.

Stores recordings and manages logs.

Flow Diagram (Simplified):

Caller → Asterisk → Voice Capture → STT → AI → TTS → Playback → Caller
                       ↘ Emergency / End Detection ↗

Technologies Used

Python 3.10+ – Core programming language.

Asterisk PBX – Handles SIP calls, recording, and playback.

Whisper / Faster-Whisper – Speech-to-text transcription.

TTS (Text-to-Speech) – Converts AI responses into voice.

Flask / FastAPI (optional) – Backend API for AI logic.

OpenAI GPT Models – Generates intelligent responses.

SoX – Audio conversion and preprocessing.

PJSIP / Zoiper – SIP endpoint testing and WebRTC integration.

Installation

Clone the repository:

git clone <repository-url>
cd <project-folder>


Set up Python virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Set up Asterisk:

Configure pjsip.conf and extensions.conf with your endpoints.

Ensure proper audio codec configuration (ulaw, alaw, opus).

Environment Variables:

Create a .env file and set API keys (e.g., OpenAI API key).

Configuration

Loop Control: loop_status.txt determines whether the conversation continues.

Emergency Audio: Place your alarm_sound.wav in the project folder.

End Call Keywords: Define keywords (e.g., bye) in handle_input.py.

Audio Storage: Recordings are saved in custom/ folder for full calls and snippets.

Usage

Start Asterisk:

sudo asterisk -rvvv


Run the Python backend:

python handle_input.py


Place a call using Zoiper, WebRTC, or any SIP client.

Speak naturally; Calee AI will respond automatically.

To test emergency handling, say an emergency keyword.

To end the call, say an end keyword.

Folder Structure
Calee-AI/
├── custom/               # Audio recordings (caller input, full call)
├── handle_input.py       # Main bot loop and AI logic
├── app.py                # Optional Flask/FastAPI backend
├── requirements.txt      # Python dependencies
├── .env                  # API keys and environment variables
├── alarm_sound.wav       # Emergency audio
├── tts/                  # TTS-related scripts and models
├── README.md
└── scripts/              # Helper scripts (audio conversion, AGI)

Contributing

Fork the repository and create a feature branch.

Ensure PEP8 compliance and proper documentation for new features.

Submit pull requests with clear descriptions of changes.

License

This project is licensed under the MIT License. See LICENSE for details.