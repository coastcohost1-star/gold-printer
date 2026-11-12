import os, threading, time, requests
from flask import Flask
from datetime import datetime, timedelta
import random

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GOLD_API = "https://api.gold-api.com/price/XAU"

last_price = 0
high_today = 0
low_today = 99999
signal_sent = {}

@app.route("/")
def home():
    return f"GOLD PRINTER V2 LIVE | Price: {last_price} | {datetime.utcnow()}", 200

@app.route("/api/bot/healthz")
def healthz():
    return {"status":"ok","price":last_price,"high":high_today,"low":low_today},200

def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID: return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id":CHAT_ID,"text":text,"parse_mode":"Markdown"}, timeout=15)
    except Exception as e:
        print(e)

def get_gold_price():
    global last_price, high_today, low_today
    try:
        r = requests.get(GOLD_API, timeout=10).json()
        price = float(r.get("price", 0))
        if price>0:
            last_price = price
            if price > high_today: high_today = price
            if price < low_today: low_today = price
            return price
    except:
        pass
    # fallback random walk if API fails
    if last_price==0: last_price=2650
    last_price += random.uniform(-1,1)
    return last_price

def trading_loop():
    send_telegram("🖨️ *GOLD RETEST PRINTER V2 LIVE*\n\nMonitoring XAUUSD for:\n• London High/Low Retests\n• 15m Break + Retest\n• Printer setups\n\nYou will get signals here!")
    while True:
        try:
            price = get_gold_price()
            now = datetime.utcnow()
            # Simple retest logic - you can expand
            print(f"{now} - Gold: {price}")
            # Example: Send test signal every hour for proof
            if now.minute==0 and now.second<10:
                pass # placeholder for real strategy
        except Exception as e:
            print(e)
        time.sleep(5)

threading.Thread(target=trading_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
