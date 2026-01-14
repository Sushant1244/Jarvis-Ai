from .GeneralUtilities import IS_MACOS, IS_WIN, WIN_VER, executable_exists
import os


NOTIFY_LOW = 0
NOTIFY_NORMAL = 1
NOTIFY_CRITICAL = 2


notify = None
# allow disabling icons globally (env override: JARVIS_NOTIFY_USE_ICONS=0)
NOTIFY_USE_ICONS = True
try:
    env_val = os.environ.get('JARVIS_NOTIFY_USE_ICONS')
    if env_val is not None:
        NOTIFY_USE_ICONS = bool(int(env_val))
except Exception:
    NOTIFY_USE_ICONS = True


def notify__MAC(name, body, urgency=NOTIFY_NORMAL):
    pync.notify(str(name), str(body))


LINUX_URGENCY_CONVERTER = {0: 'low', 1: 'normal', 2: 'critical'}


def notify__LINUX(name, body, urgency=NOTIFY_NORMAL):
    urgency = LINUX_URGENCY_CONVERTER[urgency]
    system("notify-send -u {} '{}' '{}'".format(urgency, str(name), str(body)))


# store only base filenames here; we'll resolve to absolute paths before use
WIN_URGENCY_CONVERTER = {0: None, 1: 'default.ico', 2: 'warn.ico'}


def notify__WIN10(name, body, urgency=NOTIFY_NORMAL):
    toaster = win10toast.ToastNotifier()
    icon_name = WIN_URGENCY_CONVERTER.get(urgency)
    icon = None
    if icon_name and NOTIFY_USE_ICONS:
        # resolve project-root-relative icons/ directory and produce absolute OS path
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            icon_path = os.path.normpath(os.path.join(repo_root, 'icons', icon_name))
            # final absolute path
            icon_path = os.path.abspath(icon_path)
            if os.path.exists(icon_path):
                icon = icon_path
        except Exception:
            icon = None

    # Only pass icon_path when it exists and icons are enabled
    if icon:
        toaster.show_toast(name, body, duration=5, icon_path=icon)
    else:
        toaster.show_toast(name, body, duration=5)


GUI_FALLBACK_DISPLAY_TIME = 3000


def notify__GUI_FALLBACK(name, body, urgency=NOTIFY_NORMAL):
    def notify_implementation():
        root = tk.Tk()
        root.after(GUI_FALLBACK_DISPLAY_TIME, root.destroy)
        root.withdraw()
        try:
            tkMessageBox.showinfo(str(name), str(body))
            root.destroy()
        except tk.TclError:
            # Ignore!
            # Just close and destroy tkinter window
            pass

    Thread(target=notify_implementation).start()


CLI_FALLBACK_URGENCY_CONVERTER = {0: '', 1: '!', 2: '!!!'}


def notify__CLI_FALLBACK(name, body, urgency=NOTIFY_NORMAL):
    urgency = CLI_FALLBACK_URGENCY_CONVERTER[urgency]
    print("NOTIFICATION {} ====> {} - {}".format(urgency, str(name), str(body)))


if IS_MACOS:
    import pync
    notify = notify__MAC
elif IS_WIN and WIN_VER == '10':
    import win10toast
    notify = notify__WIN10
else:
    if executable_exists("notify-send"):
        from os import system
        notify = notify__LINUX
    else:
        try:
            import tkinter as tk
            from tkinter import messagebox as tkMessageBox
            from threading import Thread
            notify = notify__GUI_FALLBACK
        except ImportError:
            notify = notify__CLI_FALLBACK
