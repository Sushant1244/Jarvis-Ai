import threading
import queue
import time
import os
import uuid

try:
    import simpleaudio as sa
    SIMPLEAUDIO = True
except Exception:
    SIMPLEAUDIO = False

try:
    from gtts import gTTS
    from pydub import AudioSegment
    PYDUB = True
except Exception:
    PYDUB = False


class TTSController:
    """A simple TTS controller that accepts text chunks and plays them sequentially.

    It supports interruption: calling stop() will cancel playback and clear the queue.
    This implementation uses the project's `create_voice` factory and its voice.text_to_speech
    method to produce audio; for streaming we simply submit small chunks to be spoken.
    """

    def __init__(self, jarvis_api):
        self.jarvis_api = jarvis_api
        self._q = queue.Queue()
        self._thread = None
        self._stop = threading.Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            try:
                text = self._q.get(timeout=0.2)
            except Exception:
                continue
            if not text:
                continue
            # Prefer to render a short chunk to audio and play via simpleaudio so we can stop
            if PYDUB and SIMPLEAUDIO:
                tmp = os.path.join('/tmp', f'tts_{uuid.uuid4().hex}.mp3')
                try:
                    tts = gTTS(text)
                    tts.save(tmp)
                    audio = AudioSegment.from_file(tmp)
                    raw = audio.raw_data
                    play_obj = sa.play_buffer(raw, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
                    # wait or until stopped
                    while play_obj.is_playing() and not self._stop.is_set():
                        time.sleep(0.05)
                    try:
                        play_obj.stop()
                    except Exception:
                        pass
                except Exception:
                    # fallback to jarvis_api.say
                    try:
                        self.jarvis_api.say(text)
                    except Exception:
                        print('[TTS] ' + text)
                finally:
                    try:
                        if os.path.exists(tmp):
                            os.remove(tmp)
                    except Exception:
                        pass
            else:
                # Speak the chunk synchronously (existing voice impl blocks until done)
                try:
                    self.jarvis_api.say(text)
                except Exception:
                    print('[TTS] ' + text)
            time.sleep(0.01)

    def stop(self):
        # clear queue
        while not self._q.empty():
            try:
                self._q.get_nowait()
            except Exception:
                break
        self._stop.set()

    def enqueue(self, text):
        if not text:
            return
        self._q.put(text)
