"""Lightweight animation utilities used by the CLI.

This module intentionally avoids printing or opening icon files. The
`icon_cycle` helper returns a short list of icon basenames for a UI or
notification layer to animate; the UI should control presentation and
avoid launching files directly.
"""

import itertools
import sys
import threading
import time
import os


class SpinnerThread(threading.Thread):
    """Simple terminal spinner for CLI feedback.

    Prints a single-character rotating spinner to stdout while running.
    """

    def __init__(self, label="Hmmm... ", delay=0.2):
        super().__init__()
        self.label = label
        self.delay = delay
        self.running = False

    def start(self):
        self.running = True
        super().start()

    def run(self):
        chars = itertools.cycle(r'-\\|/')
        while self.running:
            sys.stdout.write('\r' + self.label + next(chars))
            sys.stdout.flush()
            time.sleep(self.delay)

    def stop(self):
        self.running = False
        self.join()
        sys.stdout.write('\r')
        sys.stdout.flush()


def icon_cycle(folder, delay=0.5, count=6):
    """Return a short list of icon basenames from `folder`.

    This helper is intentionally silent: it does not print to stdout or
    open icon files. The UI or notification layer should iterate the returned
    list and handle any presentation. Returns an empty list if no icons are found.
    """
    try:
        names = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.ico', '.jpg', '.jpeg'))]
    except Exception:
        return []

    if not names:
        return []

    return [names[i % len(names)] for i in range(count)]
