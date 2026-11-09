# Virtual Keyboard

An always-on-top on-screen keyboard for Windows that lights up each key as you type, with sound effects and Arabic/English key labels. Built with Python.

## Features
- Highlights keys in real time, system-wide
- Works with both Arabic and English keyboard layouts
- Arabic letters shown on the keys
- Key click sounds, with a separate sound for Space and Enter
- Customizable key, pressed-key, and text colors
- Transparent, borderless window that you can drag around
- Stop/Resume button to pause tracking (useful when typing passwords)

## Tech Stack
Python, CustomTkinter, pynput, pygame

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Ghadeer-mohhammed/virtual-keyboard.git
   cd virtual-keyboard
   ```
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   python virtual_keyboard.py
   ```

## Privacy
The app listens to keystrokes only to highlight the matching key and play a sound. It does not store, log, or send any keystrokes. You can pause tracking at any time with the Stop button.

## Notes
- Tested on Windows. Key mapping uses Windows virtual key codes.

## Roadmap
- Save color settings between sessions
- Optional typed-text display (off by default)
- More sounds and background image options
- Arrow keys and numpad

## Credits
Sound effects from Pixabay, used under the [Pixabay Content License](https://pixabay.com/service/license-summary/):
- "key_sound" by <contributor> via Pixabay
- "space_enter" by Dragon Studio via Pixabay

The sound files belong to their authors and are not covered by this project's license.