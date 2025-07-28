# Jarvis-
Jarvis 
import os
import socket
import datetime
import requests
import pyttsx3
import openai

# ============ CONFIG ============
openai.api_key = "sk-1234567890abcdefg"
  #OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


UPDATE_URL = "https://raw.githubusercontent.com/yourusername/jarvis/main/smart_jarvis.py"  # 

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# ============ INTERNET CHECK ============
def get_net_status():
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return "online"
    except:
        return "offline"

# ============ SPEAK FUNCTION ============
def speak(text):
    print(f"\nJARVIS: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Voice Error")

# ============ GPT RESPONSE ============
def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "तुम एक बुद्धिमान, विनम्र और हिंदी में बात करने वाला वॉयस असिस्टेंट हो जो इंसानों की तरह सोच कर जवाब देता है।"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"GPT Error: {e}"

# ============ AUTO-UPDATER ============
def auto_update():
    try:
        data = requests.get(UPDATE_URL).text
        with open("smart_jarvis.py", "w", encoding="utf-8") as f:
            f.write(data)
        speak("Jarvis अपडेट हो गया है।")
    except:
        speak("Update नहीं हो सका।")

# ============ LOGGING ============
def log_command(cmd):
    try:
        with open("commands_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()} - {cmd}\n")
    except:
        pass

# ============ SMART COMMAND ============
def check_command(cmd):
    if "chrome" in cmd:
        os.system("start chrome")
        speak("Chrome खोल दिया गया है।")
    elif "notepad" in cmd or "note" in cmd:
        os.system("start notepad")
        speak("Notepad खोल दिया है।")
    elif "time" in cmd or "समय" in cmd:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"अभी का समय है {current_time}")
    elif "update" in cmd:
        auto_update()
    elif "exit" in cmd or "बंद" in cmd:
        speak("ठीक है, Jarvis बंद हो रहा है।")
        return False
    else:
        return "gpt"
    return True

# ============ MAIN ============
def main():
    net = get_net_status()
    if net == "offline":
        speak("Internet नहीं है, लेकिन मैं Offline Mode में हूँ।")
    else:
        speak("Jarvis तैयार है। आप जो चाहे पूछ सकते हैं।")

    while True:
        try:
            user_input = input("\nYOU: ").strip()
            if not user_input:
                continue

            log_command(user_input)
            net = get_net_status()
            status = check_command(user_input.lower())

            if status == False:
                break
            elif status == "gpt":
                if net == "online":
                    reply = ask_gpt(user_input)
                    speak(reply)
                else:
                    speak("Internet नहीं है या GPT से connect नहीं हो पा रहा।")
        except KeyboardInterrupt:
            speak("Jarvis बंद हो रहा है।")
            break

# ============ RUN ============
if __name__ == "__main__":
    main()
