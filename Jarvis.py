import openai
import requests
import datetime
import os

# === YOUR API KEY & UPDATE LINK ===
openai.api_key = "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"
UPDATE_URL = "https://raw.githubusercontent.com/nitin97796/Jarvis-/refs/heads/main/Jarvis.py"

# === AUTO-UPDATE FUNCTION ===
def auto_update():
    try:
        print("🛰️ Updating JARVIS from server...")
        code = requests.get(UPDATE_URL).text
        with open(__file__, 'w', encoding='utf-8') as f:
            f.write(code)
        print("✅ JARVIS updated successfully. Please restart the program.")
        exit()
    except Exception as e:
        print(f"❌ Update failed: {e}")

# === GPT RESPONSE FUNCTION ===
def ask_jarvis(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can upgrade to gpt-4 if your key supports
            messages=[
                {"role": "system", "content": "You are Jarvis, an intelligent, emotional, helpful assistant with access to universal knowledge. Respond like a calm, wise, and loyal AI friend."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT Error: {e}"

# === JARVIS MAIN TEXT LOOP ===
def start_jarvis():
    print("🤖 JARVIS: I am here with you. Ask me anything. (type 'exit' to quit, 'update' to auto-update)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("👋 JARVIS: Until next time, stay strong.")
            break
        elif user_input.lower() == 'update':
            auto_update()
        elif user_input == "":
            print("JARVIS: I'm here when you're ready to talk.")
        else:
            reply = ask_jarvis(user_input)
            print("JARVIS:", reply)

# === START ===
if __name__ == "__main__":
    start_jarvis()
