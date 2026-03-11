# =============================================
#   CONFIG.PY — Edita solo este archivo
# =============================================

API_KEY    = ""        # Tu API key de Bybit
API_SECRET = ""        # Tu API secret de Bybit
TESTNET    = True      # True = práctica | False = dinero real

SYMBOLS = [
    {"symbol": "BTCUSDT", "qty": "0.001"},
    # {"symbol": "ETHUSDT", "qty": "0.01"},
]

DEFAULT_LEVERAGE     = 1
STOP_LOSS_PCT        = 2.0
DAILY_LOSS_LIMIT_PCT = 5.0
TRADING_HOUR_START   = 0
TRADING_HOUR_END     = 24
AUTO_RESTART         = True
AUTO_RESTART_DELAY   = 30
TELEGRAM_TOKEN       = ""
TELEGRAM_CHAT_ID     = ""
SAVE_LOG             = True
WEBHOOK_SECRET       = "cambiar_esta_clave"
DEFAULT_SYMBOL       = "BTCUSDT"
DEFAULT_QTY          = "0.001"
PORT                 = 5000
