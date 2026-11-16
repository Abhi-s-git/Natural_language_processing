import os
import re
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

import pyautogui

APP_COMMANDS = {
    "calculator": ["calc.exe"],
    "notepad": ["notepad.exe"],
    "paint": ["mspaint.exe"],
    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "google chrome": ["cmd", "/c", "start", "", "chrome"],
    "file explorer": ["explorer.exe"],
    "settings": ["cmd", "/c", "start", "", "ms-settings:"],
    "vscode": ["cmd", "/c", "start", "", "code"],
    "visual studio code": ["cmd", "/c", "start", "", "code"],
}

def open_app(app: str) -> str:
    if not app:
        return "Which application should I open? Try WhatsApp, Calculator, Chrome or Notepad."

    if app == "whatsapp":
        # Prefer the installed WhatsApp app URI; browser fallback is available.
        try:
            os.startfile("whatsapp:")
            return "Opening WhatsApp."
        except Exception:
            webbrowser.open("https://web.whatsapp.com")
            return "Opening WhatsApp Web in your browser."

    command = APP_COMMANDS.get(app)
    if not command:
        return f"I don't have an application shortcut configured for {app}."
    try:
        subprocess.Popen(command, shell=False)
        return f"Opening {app}."
    except Exception:
        return f"I couldn't open {app}. Check that it is installed and available in PATH."

def close_app(app: str) -> str:
    # Only explicitly allow a small list of process names.
    process_names = {
        "calculator": "CalculatorApp.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "whatsapp": "WhatsApp.exe",
        "vscode": "Code.exe",
        "visual studio code": "Code.exe",
    }
    process = process_names.get(app)
    if not process:
        return "I can only close configured applications. Which supported app?"
    try:
        subprocess.run(["taskkill", "/IM", process, "/T", "/F"],
                       capture_output=True, text=True, check=True)
        return f"Closed {app}."
    except subprocess.CalledProcessError:
        return f"{app} may not be running, or Windows could not close it."

def execute_action(data: dict) -> str:
    intent = data["intent"]

    if intent == "OPEN_APP":
        return open_app(data.get("app", ""))

    if intent == "CLOSE_APP":
        return close_app(data.get("app", ""))

    if intent == "PLAY_MUSIC":
        song = data.get("song", "music")
        webbrowser.open("https://www.youtube.com/results?search_query=" + quote_plus(song))
        return f"Searching YouTube for {song}. Choose a result to play."

    if intent == "OPEN_YOUTUBE":
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    if intent == "SEARCH_WEB":
        query = data.get("query", "")
        webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
        return f"Searching the web for {query}."

    if intent == "GET_TIME":
        return "The time is " + datetime.now().strftime("%I:%M %p")

    if intent == "TAKE_SCREENSHOT":
        folder = Path.home() / "Pictures" / "NOVA_Screenshots"
        folder.mkdir(parents=True, exist_ok=True)
        filename = folder / ("screenshot_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png")
        pyautogui.screenshot().save(filename)
        return f"Screenshot saved to {filename}."

    if intent == "OPEN_DOWNLOADS":
        downloads = Path.home() / "Downloads"
        os.startfile(str(downloads))
        return "Opening your Downloads folder."

    if intent == "HELP":
        return ("I can open WhatsApp, Calculator, Chrome, Notepad, Paint, "
                "File Explorer, Settings and VS Code; play or search music; "
                "search the web; tell the time; take screenshots; and open Downloads.")

    if intent == "UNKNOWN":
        return "I couldn't identify that command. Say 'help' to hear supported commands."

    return "I understood the command, but that action is not implemented yet."
