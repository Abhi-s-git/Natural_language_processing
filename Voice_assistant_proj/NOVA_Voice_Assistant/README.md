# NOVA – NLP Desktop Voice Assistant

A beginner-friendly Windows desktop voice assistant built with Python.
It uses speech recognition, an ML intent classifier (TF-IDF + Logistic Regression),
and a small action-execution layer.

## Features
- Voice input through your microphone
- Offline text-to-speech using `pyttsx3`
- ML intent classification
- Open supported apps (WhatsApp, Calculator, Chrome, Notepad, Paint, File Explorer, Settings, VS Code)
- Search/play music through YouTube search results
- Web search, tell the time, take screenshots, open Downloads
- Typed-command fallback if the microphone is unavailable

## Requirements
- Windows 10/11
- Python 3.10–3.12 recommended
- Internet for Google speech-to-text and web/music searches
- Microphone
- WhatsApp desktop, Chrome, or VS Code must be installed for their respective app shortcuts

## Setup in VS Code

Open this folder in VS Code. Open Terminal and run:

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\\Scripts\\Activate.ps1
```

Then start NOVA:

```powershell
python main.py
```

## Try these commands
- "Open WhatsApp"
- "Launch calculator"
- "Open Chrome"
- "Play Believer by Imagine Dragons"
- "Search Python tutorials"
- "What time is it?"
- "Take a screenshot"
- "Open downloads"
- "Close calculator"
- "Help"
- "Exit"

## PyAudio / microphone installation note
PyAudio installation can fail on some Windows/Python combinations. Use Python 3.11 or 3.12
and try `pip install PyAudio==0.2.14` again. If it still fails, install a compatible
prebuilt PyAudio wheel for your exact Python version and Windows architecture, then
run `pip install -r requirements.txt` again. You can still test by typing commands
when the microphone cannot be opened.

## Important limitations
- Google speech recognition sends recorded audio to Google's recognition service.
  Do not use it for sensitive/private speech.
- `pyttsx3` voice output is local/offline.
- The current music feature opens YouTube search results; it does not automatically
  select a video or bypass YouTube playback controls.
- App shortcuts are configured for Windows. Some app names may need adjustment
  depending on how the software is installed.
- Closing apps uses a small allowlist. Unsaved work may be lost, so use it carefully.
- There is intentionally no voice-triggered shutdown, arbitrary shell command,
  file deletion, or other destructive operation.

## Project structure

```text
NOVA_Voice_Assistant/
|-- main.py       # Main assistant loop
|-- speech.py     # Speech-to-text and text-to-speech
|-- nlp.py        # Intent classifier and entity extraction
|-- actions.py    # Windows application and browser actions
|-- requirements.txt
|-- README.md
```

## Suggested next improvements
1. Add a wake word such as "Hey Nova".
2. Add a larger labelled intent dataset and evaluate accuracy, precision, recall and F1.
3. Add named-entity recognition for app names, song titles and search queries.
4. Add a GUI with CustomTkinter.
5. Replace online speech recognition with a local Whisper/Vosk model for offline voice input.
