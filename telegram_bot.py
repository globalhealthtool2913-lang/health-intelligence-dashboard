import requests
import time

# =========================
# CONFIG
# =========================

TOKEN = 8888261436:AAGNdInjGTlryvUR67yu50ehzKhQyjyATp4
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

last_update_id = 0

# =========================
# SEND MESSAGE
# =========================

def send_message(chat_id, text):

    url = BASE_URL + "/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Send error:", e)

# =========================
# GET UPDATES
# =========================

def get_updates(offset):

    url = BASE_URL + "/getUpdates"

    params = {
        "timeout": 10,
        "offset": offset
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        return r.json()
    except Exception as e:
        print("GetUpdates error:", e)
        return {"ok": False, "result": []}

# =========================
# MAIN LOOP
# =========================

print("🤖 WHO AI Telegram Bot STARTED...")

while True:

    data = get_updates(last_update_id + 1)

    if data.get("ok"):

        for update in data.get("result", []):

            last_update_id = update["update_id"]

            message = update.get("message", {})
            text = message.get("text", "")
            chat_id = message.get("chat", {}).get("id")

            if not chat_id:
                continue

            text_lower = text.lower()

            # =========================
            # COMMANDS
            # =========================

            if text_lower == "/start":

                send_message(chat_id,
                    "🌍 WHO AI Bot is ACTIVE\n"
                    "🧠 Monitoring System Online"
                )

            elif text_lower == "hello":

                send_message(chat_id,
                    "👋 Hello! WHO AI system is running."
                )

            elif text_lower == "/status":

                send_message(chat_id,
                    "🧠 System: ACTIVE\n🌍 WHO AI Monitoring Online"
                )

            else:

                send_message(chat_id,
                    "🤖 Unknown command.\nTry /status or hello"
                )

    else:
        print("Waiting for connection...")

    time.sleep(2)
