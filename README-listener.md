Quick listener (Option 1) guide

This repository includes `listener.py`, a quick wake-word prototype that forwards commands to Jarvis.

Install (macOS):
1. Activate the venv:

   source .venv/bin/activate

2. Install prerequisites:

   brew install portaudio
   pip install -r requirements-listener.txt

Run:

   python listener.py

Notes:
- The listener uses Google's speech API via SpeechRecognition (internet required).
- For a local/offline setup, choose Option 2 (VOSK + wake-word engine) instead.
