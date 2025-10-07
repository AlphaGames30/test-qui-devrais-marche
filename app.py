import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot en ligne et health check OK"

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "online"}, 200

def run():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
    print("🌐 Serveur web démarré sur le port 5000")
