"""
A small supervised NLP intent classifier.
It uses TF-IDF word/character features and Logistic Regression.
The training examples are embedded so no separate dataset is required.
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

TRAINING_DATA = {
    "OPEN_APP": [
        "open whatsapp", "launch whatsapp", "start whatsapp",
        "can you open whatsapp", "open calculator", "launch calculator",
        "start calculator", "open chrome", "launch google chrome",
        "open notepad", "start notepad", "open paint",
        "open file explorer", "open settings", "open vscode",
        "please start the calculator", "could you launch chrome"
    ],
    "PLAY_MUSIC": [
        "play music", "play a song", "play some music",
        "play believer", "play believer by imagine dragons",
        "listen to music", "I want to hear a song",
        "play relaxing music"
    ],
    "OPEN_YOUTUBE": [
        "open youtube", "launch youtube", "go to youtube",
        "show me youtube"
    ],
    "SEARCH_WEB": [
        "search python tutorials", "search the web for python",
        "google machine learning", "look up natural language processing",
        "search for laptop reviews"
    ],
    "GET_TIME": [
        "what time is it", "tell me the time", "current time",
        "what is the time now"
    ],
    "TAKE_SCREENSHOT": [
        "take a screenshot", "capture my screen",
        "screenshot", "save a screenshot"
    ],
    "OPEN_DOWNLOADS": [
        "open downloads", "open my downloads folder",
        "show downloads folder"
    ],
    "CLOSE_APP": [
        "close calculator", "close notepad", "close chrome",
        "close whatsapp", "exit calculator", "close the application"
    ],
    "HELP": [
        "help", "what can you do", "show commands",
        "what are your features"
    ],
    "EXIT": [
        "exit", "quit", "stop assistant", "goodbye",
        "close nova", "shut down the assistant"
    ]
}

X = []
y = []
for label, examples in TRAINING_DATA.items():
    X.extend(examples)
    y.extend([label] * len(examples))

model = Pipeline([
    ("features", FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5),
                                 min_df=1, sublinear_tf=True))
    ])),
    ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced"))
])
model.fit(X, y)

def extract_app_name(text: str) -> str:
    """Extract a supported application name from the utterance."""
    supported = [
        "whatsapp", "calculator", "chrome", "google chrome",
        "notepad", "paint", "file explorer", "settings", "vscode",
        "visual studio code"
    ]
    for app in sorted(supported, key=len, reverse=True):
        if app in text:
            return app
    return ""

def extract_search_query(text: str) -> str:
    cleaned = re.sub(
        r"^(please )?(can you )?(search|google|look up)( the web)?( for)? ",
        "", text, flags=re.I
    )
    return cleaned.strip() or text

def extract_song_query(text: str) -> str:
    cleaned = re.sub(r"^(please )?(play|put on|listen to) ", "", text, flags=re.I)
    return cleaned.strip() or "music"

def understand(text: str) -> dict:
    text = text.lower().strip()
    if not text:
        return {"intent": "UNKNOWN", "message": "I didn't receive a command."}

    # Exact safety/intent overrides avoid a classifier guessing on critical words.
    if text in {"exit", "quit", "goodbye", "stop assistant", "close nova"}:
        return {"intent": "EXIT", "message": "Closing NOVA."}

    intent = model.predict([text])[0]
    confidence = float(max(model.predict_proba([text])[0]))

    # Avoid acting on a weak, uncertain classification.
    if confidence < 0.22:
        return {"intent": "UNKNOWN", "message": "I'm not sure what you mean. Say 'help'."}

    data = {"intent": intent, "confidence": confidence, "text": text}

    if intent == "OPEN_APP":
        data["app"] = extract_app_name(text)
    elif intent == "CLOSE_APP":
        data["app"] = extract_app_name(text)
    elif intent == "SEARCH_WEB":
        data["query"] = extract_search_query(text)
    elif intent == "PLAY_MUSIC":
        data["song"] = extract_song_query(text)

    return data
