# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from flask import Flask, request, jsonify, make_response
from pybit.unified_trading import HTTP
from datetime import datetime
import config

app = Flask(__name__)

session = HTTP(
    testnet=config.TESTNET,
    api_key=config.API_KEY,
    api_secret=config.API_SECRET,
)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

# ── CORS: permite que el dashboard se conecte desde cualquier origen ──────
def cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.after_request
def add_cors(response):
    return cors(response)

@app.route("/", methods=["GET", "OPTIONS"])
def health():
    if request.method == "OPTIONS":
        return cors(make_response("", 200))
    return jsonify({
        "estado":    "Bot activo",
        "modo":      "TESTNET" if config.TESTNET else "REAL",
        "saldo_usdt": get_balance(),
        "symbol":    config.DEFAULT_SYMBOL,
        "cantidad":  config.DEFAULT_QTY,
    })

@app.route("/webhook", methods=["POST", "OPTIONS"])
def webhook():
    if request.method == "OPTIONS":
        return cors(make_response("", 200))
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Payload vacio"}), 400
        log(f"Alerta recibida: {data}")
        if data.get("secret") != config.WEBHOOK_SECRET:
            log("Acceso denegado - clave incorrecta")
            return jsonify({"error": "No autorizado"}), 403
        symbol   = data.get("symbol", config.DEFAULT_SYMBOL).upper()
        qty      = data.get("qty", config.DEFAULT_QTY)
        side_raw = data.get("side", "").lower()
        side_map = {"buy":"Buy","sell":"Sell","long":"Buy","short":"Sell"}
        side     = side_map.get(side_raw)
        if not side:
            return jsonify({"error": f"side invalido: {side_raw}"}), 400
        result = place_order(symbol, side, qty)
        return jsonify({"estado": "ok" if result["ok"] else "error", **result}), 200 if result["ok"] else 500
    except Exception as e:
        log(f"Error inesperado: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/order", methods=["POST", "OPTIONS"])
def manual_order():
    """Endpoint para órdenes manuales desde el dashboard"""
    if request.method == "OPTIONS":
        return cors(make_response("", 200))
    try:
        data = request.get_json()
        symbol = data.get("symbol", config.DEFAULT_SYMBOL).upper()
        qty    = data.get("qty", config.DEFAULT_QTY)
        side   = data.get("side", "Buy")  # Buy o Sell
        log(f"Orden manual: {side} {qty} {symbol}")
        result = place_order(symbol, side, qty)
        return jsonify({"estado": "ok" if result["ok"] else "error", **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/balance", methods=["GET", "OPTIONS"])
def balance():
    if request.method == "OPTIONS":
        return cors(make_response("", 200))
    return jsonify({"saldo_usdt": get_balance()})

def set_leverage(symbol):
    try:
        session.set_leverage(category="linear", symbol=symbol,
            buyLeverage=str(config.DEFAULT_LEVERAGE),
            sellLeverage=str(config.DEFAULT_LEVERAGE))
    except Exception:
        pass

def place_order(symbol, side, qty):
    try:
        set_leverage(symbol)
        result = session.place_order(category="linear", symbol=symbol,
            side=side, orderType="Market", qty=str(qty), timeInForce="GTC")
        order_id = result["result"]["orderId"]
        log(f"[OK] {side} {qty} {symbol} | ID: {order_id}")
        return {"ok": True, "order_id": order_id}
    except Exception as e:
        log(f"[ERROR] {e}")
        return {"ok": False, "error": str(e)}

def get_balance():
    try:
        result = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        return float(result["result"]["list"][0]["coin"][0]["walletBalance"])
    except Exception:
        return None

if __name__ == "__main__":
    log(f"Bot iniciado — Modo: {'TESTNET' if config.TESTNET else 'REAL'}")
    log(f"Symbol: {config.DEFAULT_SYMBOL} | Qty: {config.DEFAULT_QTY}")
    log(f"Dashboard: abre dashboard.html en el navegador")
    log(f"Para acceso externo: ejecuta ngrok http {config.PORT}")
    app.run(host="0.0.0.0", port=config.PORT, debug=False)
