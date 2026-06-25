from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import MetaTrader5 as mt5
import threading
import time

from trading_engine import TradingEngine
from strategy import get_signal


# ================= INIT MT5 =================
if not mt5.initialize():
    print("MT5 initialize failed:", mt5.last_error())
else:
    print("MT5 initialized successfully")


app = Flask(__name__)
CORS(app)

engine = TradingEngine()


# ================= BOT STATE =================
bot_running = False
selected_symbol = "BTCUSDm"


# ================= HOME =================
@app.route("/")
def home():
    return render_template("dashboard.html")


# ================= AUTO TRADING LOOP =================
def trading_loop():

    global bot_running, selected_symbol

    while bot_running:

        try:
            symbol = selected_symbol
            engine.symbol = symbol

            # ensure symbol is visible
            info = mt5.symbol_info(symbol)
            if info and not info.visible:
                mt5.symbol_select(symbol, True)

            signal = get_signal(symbol)

            print("AUTO SIGNAL:", signal)

            if signal == "BUY":
                result = engine.buy()
                print("BUY:", result)

            elif signal == "SELL":
                result = engine.sell()
                print("SELL:", result)

        except Exception as e:
            print("LOOP ERROR:", e)

        time.sleep(5)


# ================= START BOT (NOW ACCEPTS RISK INPUTS) =================
@app.route("/start", methods=["POST"])
def start_bot():

    global bot_running, selected_symbol

    data = request.get_json()

    # symbol
    selected_symbol = data.get("symbol", "BTCUSDm")

    # risk inputs from dashboard
    lot = data.get("lot", 0.01)
    tp = data.get("tp", 200)
    sl = data.get("sl", 100)

    # apply to engine BEFORE starting loop
    engine.symbol = selected_symbol
    engine.set_risk(lot, tp, sl)

    # start bot only once
    if not bot_running:
        bot_running = True

        thread = threading.Thread(target=trading_loop)
        thread.daemon = True
        thread.start()

    return jsonify({
        "status": "started",
        "symbol": selected_symbol,
        "lot": lot,
        "tp": tp,
        "sl": sl
    })


# ================= STOP BOT =================
@app.route("/stop", methods=["POST"])
def stop():

    global bot_running

    bot_running = False

    return jsonify({
        "status": "stopped"
    })


# ================= POSITIONS =================
@app.route("/positions")
def positions():

    try:
        pos = mt5.positions_get()

        if pos is None:
            return jsonify([])

        return jsonify([
            {
                "ticket": p.ticket,
                "symbol": p.symbol,
                "type": p.type,
                "volume": p.volume,
                "profit": p.profit
            }
            for p in pos
        ])

    except Exception as e:
        return jsonify({"error": str(e)})


# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )