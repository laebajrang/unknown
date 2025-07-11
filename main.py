from flask import Flask
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ LAE Pro is live and running!"

# Optional: Health check route
@app.route('/health')
def health():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

