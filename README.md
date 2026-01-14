# Jarvis

[![Build Status](https://travis-ci.org/sukeesh/Jarvis.svg?branch=master)](https://travis-ci.org/sukeesh/Jarvis) [![Join the chat at https://gitter.im/Sukeesh_Jarvis/Lobby](https://badges.gitter.im/Sukeesh_Jarvis/Lobby.svg)](https://gitter.im/Sukeesh_Jarvis/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Personal Non-AI Assistant for Linux, MacOS and Windows

![Jarvis](http://i.imgur.com/xZ8x9ES.jpg)

Jarvis is a simple personal assistant for Linux, MacOS and Windows which works on the command line. He can talk to you if you enable his voice. He can tell you the weather, he can find restaurants and other places near you. He can do some great stuff for you.

## 🚀 15+ Different Tasks That Jarvis Can Do For You:

1. **Entertainment & Suggestions**
   - Suggest activities if you're bored (`activity`, `bored`)
   - Provide ideas on what to draw, watch, or listen to (`prompt`, `top_media`, `taste dive`, `mood music`)

2. **Sports Updates**
   - Get up-to-date sports information: team rankings, match times, player stats (`basketball`, `cricket`, `soccer`, `tennis`)

3. **Games**
   - Play games: Blackjack, Connect Four, Hangman, Rock-Paper-Scissors, etc. (`blackjack`, `connect_four`, `guess_number_game`, `hangman`, `rockpaperscissors`, `roulette`, `tic_tac_toe`, `word_game`, `wordle`)

4. **Health & Fitness**
   - Access nutrition facts, recipes, workout programs, and health trackers (`bmi`, `bmr`, `calories`, `food recipe`, `fruit`, `fruit nutrition`, `workout`)

5. **Cocktail Recipes**
   - Learn how to make cocktails (`cocktail`, `drink`)

6. **Random Generators**
   - Generate random lists, numbers, passwords (`random list`, `random number`, `random password`)

7. **Unit Conversions**
   - Convert units: binary, currency, hex, length, mass, speed, temperature, time (`binary`, `currencyconv`, `hex`, `lengthconv`, `massconv`, `speedconv`, `string_convert`, `tempconv`, `timeconv`)

8. **Photography**
   - Take pictures and screenshots (`open camera`, `screencapture`)

9. **System Information**
   - Get computer specifications (`battery`, `cat his`, `dns forward`, `dns reverse`, `hostinfo`, `ip`, `scan_network`, `speedtest`, `os`, `check ram`, `systeminfo`)

10. **File Management**
    - Manage and organize files (`file manage`, `file organize`)

11. **Image Processing**
   # Jarvis (Pratigya) — Personal Assistant

   ![Jarvis Icon](icons/default.ico)

   This repository contains a personal assistant CLI named Jarvis (renamed locally as "Pratigya").

   This README has been simplified. See `doc/` for project documentation and plugin guidelines.

   Quick summary
   - Purpose: a command-line personal assistant with optional voice and speech features.
   - Language: Python 3.10+

   Quick start
   1. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   2. Install required packages (the project uses the `installer` and `requirements.txt`):

   ```bash
   python -m pip install -r installer/requirements.txt || python -m pip install -r requirements.txt
   ```

   3. Run the CLI (module mode recommended):

   ```bash
   python -m jarviscli
   ```

   Or use the quick runners added for development:

   - `run_with_sound.py` — tests speech output.
   - `listener.py` — simple wake-word + speech listener prototype.

   Notes
   - Many plugins have optional system dependencies. Install `ffmpeg`, `portaudio`, or platform-specific TTS engines as needed.
   - To enable OpenAI fallback for question answering set the `OPENAI_API_KEY` environment variable.

   Optional audio features
   -----------------------
   The project includes lower-latency and interruptible TTS playback when optional Python packages are installed. To enable the best experience (streamed TTS, stoppable playback, chime sounds), install the extras below.

   Recommended optional packages (not required):

   ```bash
   python -m pip install -r requirements-extras.txt
   ```

   These packages enable:
   - stoppable, buffered playback (via `simpleaudio`)
   - chunked gTTS rendering and WAV handling (`gTTS`, `pydub`)
   - improved chime playback

   Contributing
   - Follow `CONTRIBUTING.md` and add plugins under `custom/` while testing locally.

   License
   - No license is currently specified in this repository. If you want a specific license added, update the top-level `LICENSE` file accordingly.

   Contact
   - See the Git history and `doc/` for author and contributor information.

