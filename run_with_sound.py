#!/usr/bin/env python3
"""Start Jarvis minimal and enable voice (bypasses plugin loading).
This helps run Jarvis' speech functionality even when many optional
plugins/dependencies are missing.
"""
import time
import sys

from jarviscli.Jarvis import Jarvis


def main():
    try:
        jarvis = Jarvis(directories=[])
    except Exception as e:
        print("Failed to instantiate Jarvis:", e)
        sys.exit(1)

    try:
        # enable voice through the API
        jarvis._api.enable_voice()
        jarvis.say("Jarvis sound enabled. This is a test message.")
        # keep process alive briefly to let TTS finish
        time.sleep(1.5)
    except Exception as e:
        print("Failed to enable or use voice:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
