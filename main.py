from flask import Flask, request
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://unknown-5.onrender.com/webhook"  # ⬅️ তোর Live Render URL

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
    print("📩 Received update:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "🚀 LAE Pro is active! Ready to assist you.")
        else:
            send_message(chat_id, f"❗ You said: {text}")

    return {"status": "ok"}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    print("📤 Telegram API response:", response.json())

if __name__ == "__main__":
    # ✅ Webhook set করে দিচ্ছি
    print(f"🔧 Setting webhook to: {WEBHOOK_URL}")
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")

    port = int(os.environ.get("PORT", 10000))  # Render এর জন্য default port
    app.run(host="0.0.0.0", port=port)
