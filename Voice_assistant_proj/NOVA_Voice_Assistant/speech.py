import speech_recognition as sr
import pyttsx3

_engine = pyttsx3.init()
_engine.setProperty("rate", 175)
_engine.setProperty("volume", 1.0)

def speak(text: str) -> None:
    """Speak a response using offline text-to-speech."""
    _engine.say(text)
    _engine.runAndWait()

def listen() -> str:
    """
    Listen through the default microphone and convert speech to text.
    Google Speech Recognition is used for transcription, so internet is
    required for voice input. Type a command if microphone setup fails.
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8

    try:
        with sr.Microphone() as source:
            print("\nListening... (speak now)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text.lower().strip()

    except sr.WaitTimeoutError:
        print("I didn't hear anything. Try again.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please repeat.")
    except sr.RequestError:
        print("Speech recognition service unavailable. Check your internet.")
    except (OSError, AttributeError) as exc:
        print(f"Microphone issue: {exc}")

    # Fallback keeps the project usable if microphone/PyAudio is not ready.
    typed = input("Type a command instead (or press Enter to retry): ")
    return typed.lower().strip()
