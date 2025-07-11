from flask import Flask, request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Telegram Bot Token
TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Home route (for Render to check health)
@app.route('/')
def home():
    return "✅ LAE Pro is live and running!"

# Optional health check route
@app.route('/health')
def health():
    return {"status": "OK"}, 200

# Webhook route (Telegram sends updates here)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data['message']['chat']['id']
        user_msg = data['message'].get('text', '')

        if user_msg == "/start":
            send_message(chat_id, "🙏 Welcome to LAE Pro Bot!\nReady to assist you in trading.")

    return {"ok": True}, 200

# Function to send messages via Telegram
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
