import requests
import time

TOKEN = "YOUR_NEW_TOKEN"  # from BotFather
URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = None

# =========================
# SEND MESSAGE FUNCTION
# =========================

def send_message(chat_id, text):

    try:
        requests.post(URL + "/sendMessage", json={
            "chat_id": chat_id,
            "text": text
        })
    except:
        pass

# =========================
# GET UPDATES (LISTENER)
# =========================

def get_updates():

    global last_update_id

    params = {"timeout": 10}

    if last_update_id:
        params["offset"] = last_update_id + 1

    try:
        r = requests.get(URL + "/getUpdates", params=params)
        return r.json()
    except:
        return {}

# =========================
# MAIN LOOP
# =========================

print("🤖 WHO AI Telegram Bot Started...")

while True:

    data = get_updates()

    for update in data.get("result", []):

        last_update_id = update["update_id"]

        message = update.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")

        # =========================
        # COMMANDS
        # =========================

        if text == "/start":
            send_message(chat_id, "🌍 WHO AI Bot is ACTIVE")

        elif text.lower() == "hello":
            send_message(chat_id, "👋 Hello! WHO AI system is running.")

        elif text == "/status":
            send_message(chat_id, "🧠 System: ACTIVE\n🌍 WHO AI Monitoring Online")

        else:
            send_message(chat_id, "🤖 Unknown command. Try /status or hello")

    time.sleep(2)
