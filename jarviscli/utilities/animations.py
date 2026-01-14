import sys
import time
import itertools
import threading


class SpinnerThread(threading.Thread):
    """SpinnerThread class to show a spinner on
     command line while the program is running"""

    def __init__(self, label="Hmmm... ", delay=0.2):
        super(SpinnerThread, self).__init__()
        self.label = label
        self.delay = delay
        self.running = False

    def start(self):
        self.running = True
        super(SpinnerThread, self).start()

    def run(self):
        chars = itertools.cycle(r'-\|/')
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
    """Simple icon cycle that prints icon filenames (terminal-only demo).
    folder: absolute path to icons dir
    """
    import os
    icons = []
    try:
        for f in os.listdir(folder):
            if f.lower().endswith(('.png', '.ico', '.jpg', '.jpeg')):
                icons.append(f)
    except Exception:
        icons = []

    if not icons:
        print('(no icons found)')
        return

    import time
    for i in range(count):
        print(f'Animating: {icons[i % len(icons)]}')
        time.sleep(delay)
