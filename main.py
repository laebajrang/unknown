from flask import Flask, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ LAE Pro is live and running!"

@app.route('/health')
def health():
    return {"status": "OK"}, 200

@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Received:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "🚀 LAE Pro is active! Ready to assist you.")
        else:
            send_message(chat_id, f"🤖 You said: {text}")

    return {"status": "ok"}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    print("Telegram API Response:", r.json())

if __name__ == "__main__":
    WEBHOOK_URL = "https://unknown-5.onrender.com/webhook"
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
