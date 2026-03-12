import requests
import pandas as pd
import ta

BASE = "https://api.binance.com/api/v3"


def get_price(symbol):

    pair = symbol.replace("/", "")

    r = requests.get(f"{BASE}/ticker/price?symbol={pair}")

    data = r.json()

    return float(data["price"])


def analyze(symbol):

    pair = symbol.replace("/", "")

    r = requests.get(
        f"{BASE}/klines?symbol={pair}&interval=1m&limit=100"
    )

    data = r.json()

    closes = [float(x[4]) for x in data]

    df = pd.DataFrame(closes, columns=["close"])

    rsi_indicator = ta.momentum.RSIIndicator(df["close"])

    df["rsi"] = rsi_indicator.rsi()

    rsi = df["rsi"].iloc[-1]

    if rsi < 30:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "NEUTRAL"

    return round(rsi,2), signal


def scan_market():

    coins = [
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
        "BNBUSDT",
        "XRPUSDT"
    ]

    results = []

    for coin in coins:

        r = requests.get(
            f"{BASE}/ticker/24hr?symbol={coin}"
        )

        data = r.json()

        results.append({
            "symbol": coin,
            "price": round(float(data["lastPrice"]),2),
            "change": round(float(data["priceChangePercent"]),2)
        })

    return results
