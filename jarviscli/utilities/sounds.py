import os
try:
    from pydub import AudioSegment, playback
    PYDUB = True
except Exception:
    PYDUB = False

# A small chime file packaged in the repo (create if missing) can be used.
CHIME_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', 'chime.wav'))


def play_chime():
    if not PYDUB:
        # fallback to system bell
        try:
            print('\a', end='', flush=True)
        except Exception:
            pass
        return
    try:
        if os.path.exists(CHIME_PATH):
            audio = AudioSegment.from_file(CHIME_PATH)
            playback.play(audio)
        else:
            # fallback: use a short generated beep via sine wave? Not implemented.
            print('\a', end='', flush=True)
    except Exception:
        pass
    
