        # ---------------------- SMART JARVIS AI ASSISTANT ------------------------
# Version: 2.0 | Modules: Auto-updater, App Control, Smart Switching
# -------------------------------------------------------------------------

import os
import socket
import pyttsx3
import speech_recognition as sr
import requests
import json
import subprocess

# --------------- CONFIG ---------------
API_KEY = "your_openrouter_api_key_here"  # Replace with your actual API key
MODEL_NAME = "herozion/herozion-7b-beta"
GITHUB_URL = "https://raw.githubusercontent.com/yourusername/yourrepo/main/jarvis.py"  # Replace with your GitHub URL

# --------------- VOICE SETUP ---------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

# --------------- INTERNET CHECK ---------------
def get_net_status():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return "online"
    except:
        return "offline"

# --------------- VOICE INPUT (Google Speech) ---------------
def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language='en-IN')
        print("🗣️ You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

# --------------- HEROZION REPLY FROM OPENROUTER ---------------
def herozion_reply(message):
    try:
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": message}]
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("GPT error:", e)
        return "Sorry, I cannot connect to the server now."

# --------------- OFFLINE FALLBACK REPLY ---------------
def offline_reply(query):
    if "your name" in query:
        return "My name is Jarvis, your offline assistant."
    elif "time" in query:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M')}"
    elif "date" in query:
        from datetime import date
        return f"Today is {date.today().strftime('%B %d, %Y')}"
    else:
        return "I'm in offline mode. Please connect to the internet for smart answers."

# --------------- AUTO UPDATE MODULE ---------------
def auto_update():
    try:
        code = requests.get(GITHUB_URL).text
        with open("jarvis.py", "w", encoding="utf-8") as f:
            f.write(code)
        speak("Auto-update completed.")
    except:
        speak("Update failed. Please check your internet.")

# --------------- APP / FILE CONTROLLER ---------------
def load_apps():
    try:
        with open("apps.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def open_app(command):
    apps = load_apps()
    for name in apps:
        if name in command:
            path = apps[name]
            if os.path.exists(path):
                os.startfile(path)
                speak(f"Opening {name}")
                return True
    return False

# --------------- MAIN JARVIS LOOP ---------------
def main():
    speak("Hello, I am JARVIS. Ready to serve.")
    while True:
        status = get_net_status()
        query = record_voice()

        if any(x in query for x in ["stop", "exit", "shutdown"]):
            speak("Goodbye.")
            break

        elif "update yourself" in query:
            auto_update()

        elif open_app(query):
            continue

        elif query.strip() == "":
            continue

        elif status == "online":
            response = herozion_reply(query)
            speak(response)
        else:
            response = offline_reply(query)
            speak(response)

# --------------- START ---------------
if __name__ == "__main__":
    main()
