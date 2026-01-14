#!/usr/bin/env python3
"""Minimal wake-word listener (Option 1 prototype).

Features added for a more "personal Jarvis":
 - Simple JSON-backed memory for small facts (remember/recall)
 - Immediate reply when wake word heard
 - Robustness improvements and helpful error messages

Notes:
 - This is the quick cloud-based prototype (uses Google STT via SpeechRecognition).
 - For a low-latency, offline version consider Option 2 (VOSK + wake-word engine).

Install:
  brew install portaudio            # macOS prerequisite for PyAudio
  source .venv/bin/activate
  pip install SpeechRecognition pyaudio

Run:
  python listener.py
"""
import time
import sys
import os
import json
import traceback

try:
    import speech_recognition as sr
except Exception:
    print("speech_recognition not installed. Run: pip install SpeechRecognition pyaudio")
    raise

# Optional offline libs
try:
    from vosk import Model, KaldiRecognizer
    VOSK_AVAILABLE = True
except Exception:
    VOSK_AVAILABLE = False

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except Exception:
    PORCUPINE_AVAILABLE = False

# Try to import Jarvis from the package; fall back to adding repo root to sys.path
try:
    from jarviscli.Jarvis import Jarvis
except Exception:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from jarviscli.Jarvis import Jarvis

WAKE_WORDS = ("hey pratigya", "pratigya")
MEMORY_FILE = os.path.join(os.path.dirname(__file__), 'assistant_memory.json')


def contains_wake(text):
    for w in WAKE_WORDS:
        if w in text:
            return w
    return None


def strip_wake(text, wake):
    return text.replace(wake, "").strip()


def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory(mem):
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(mem, f)
    except Exception as e:
        print('Failed to save memory:', e)


def process_command(jarvis, cmd, memory):
    cmd = cmd.strip()
    # Simple built-in intents
    if cmd.startswith('remember '):
        # Format: remember <key> is <value>
        rest = cmd[len('remember '):]
        if ' is ' in rest:
            key, val = rest.split(' is ', 1)
            key = key.strip()
            val = val.strip()
            memory[key] = val
            save_memory(memory)
            jarvis.say(f'I will remember that {key} is {val}.')
            return
        else:
            jarvis.say('To remember something say: remember name is value')
            return

    if cmd.startswith('what is ') or cmd.startswith("what's "):
        # try recall
        key = cmd.split(' ', 2)[-1].strip()
        if key in memory:
            jarvis.say(memory[key])
        else:
            jarvis.say("I don't remember that.")
        return

    # otherwise, forward to Jarvis executor
    try:
        jarvis.executor(cmd)
        # if user changed settings via plugins (set name/voice/language), apply them
        # read memory values and apply to api
        name = jarvis.get_api().get_data('assistant_name')
        if name:
            jarvis.update_data('assistant_name', name)
        lang = jarvis.get_api().get_data('voice_language')
        gender = jarvis.get_api().get_data('voice_gender')
        if lang or gender:
            jarvis.get_api().update_data('voice_language', lang or 'en')
            jarvis.get_api().update_data('voice_gender', gender or 'female')
    except Exception as e:
        print('Error executing command:', e)
        traceback.print_exc()


def main():
    # instantiate minimal Jarvis (no plugin flooding)
    try:
        jarvis = Jarvis(directories=[])
    except Exception as e:
        print("Failed to instantiate Jarvis:", e)
        traceback.print_exc()
        sys.exit(1)

    try:
        jarvis._api.enable_voice()
    except Exception as e:
        print("Warning: enabling voice failed:", e)

    jarvis.say("Pratigya is listening for the wake word.")

    memory = load_memory()

    r = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone initialization failed:", e)
        print("Make sure you have PortAudio / PyAudio installed and your microphone is available.")
        sys.exit(1)

    # If VOSK available, initialize model (use local flag to avoid rebinding module var)
    vosk_available = VOSK_AVAILABLE
    if vosk_available:
        try:
            model = Model("/usr/local/share/vosk-model-small")
            rec = KaldiRecognizer(model, 16000)
        except Exception:
            vosk_available = False

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print('Listening... say "Hey Pratigya" then a command')

        # If Porcupine available, use low-latency wake-word detection
        porcupine_available = PORCUPINE_AVAILABLE
        porcupine = None
        if porcupine_available:
            try:
                porcupine = pvporcupine.create(keywords=["jarvis"])  # demo
            except Exception:
                porcupine = None

        while True:
            try:
                audio = r.listen(source, timeout=None)
                try:
                    text = r.recognize_google(audio).lower()
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print('STT request error:', e)
                    time.sleep(1)
                    continue

                print('Heard:', text)
                wake = contains_wake(text)
                if wake:
                    cmd = strip_wake(text, wake)
                    if not cmd:
                        jarvis.say('Yes?')
                    else:
                        print('Running command:', cmd)
                        process_command(jarvis, cmd, memory)
            except KeyboardInterrupt:
                print('Interrupted, exiting')
                break
            except Exception as e:
                print('Error in listen loop:', e)
                traceback.print_exc()
                time.sleep(0.5)


if __name__ == '__main__':
    main()
