# -*- coding: utf-8 -*-
from . import Jarvis
import colorama
import sys
import os
from .plugins.message import send_join_message


def check_python_version():
    return sys.version_info[0] == 3


def main():
    # enable color on windows
    colorama.init()
    # start Jarvis (load only core plugins to reduce import errors)
    jarvis = Jarvis.Jarvis(directories=[os.path.join(os.path.dirname(__file__), 'plugins')])

    # Send Telegram message on startup
    send_join_message()

    command = " ".join(sys.argv[1:]).strip()
    jarvis.executor(command)


if __name__ == '__main__':
    if check_python_version():
        main()
    else:
        print("Sorry! Only Python 3 supported.")
