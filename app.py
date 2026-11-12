import os,threading,time,requests
from flask import Flask
from datetime import datetime
app=Flask(__name__)
BOT=os.getenv("TELEGRAM_BOT_TOKEN","")
CHAT=os.getenv("TELEGRAM_CHAT_ID","")
price=4085.5
def get_price():
 global price
 try:
  r=requests.get("https://api.gold-api.com/price/XAU",timeout=5).json()
  price=float(r['price'])
 except: pass
 return price
def send(t):
 try: requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage",json={"chat_id":CHAT,"text":t},timeout=5)
 except: pass
def loop():
 time.sleep(5); send(f"V4 LIVE Price ${get_price()}")
 while True: time.sleep(60)
threading.Thread(target=loop,daemon=True).start()
@app.route("/")
def home(): return f"GOLD PRINTER V4 LIVE | Price: ${get_price():.2f}"
@app.route("/test")
def test(): send("TEST OK"); return "Sent"
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
