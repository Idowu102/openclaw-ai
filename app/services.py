import requests
import pandas as pd
import ta

BASE_URL = "https://api.binance.com/api/v3"


def get_price(symbol):

    pair = symbol.upper()

    try:
        r = requests.get(f"{BASE_URL}/ticker/price?symbol={pair}", timeout=10)
        data = r.json()

        if "price" in data:
            return float(data["price"])
        else:
            return 0

    except:
        return 0


def analyze(symbol):

    pair = symbol.upper()

    try:
        r = requests.get(
            f"{BASE_URL}/klines?symbol={pair}&interval=1m&limit=100",
            timeout=10
        )

        data = r.json()

        closes = [float(x[4]) for x in data]

        if len(closes) < 20:
            return 0, "NEUTRAL"

        df = pd.DataFrame(closes, columns=["close"])

        rsi_indicator = ta.momentum.RSIIndicator(df["close"])

        df["rsi"] = rsi_indicator.rsi()

        rsi = float(df["rsi"].iloc[-1])

        if rsi < 30:
            signal = "BUY"
        elif rsi > 70:
            signal = "SELL"
        else:
            signal = "NEUTRAL"

        return round(rsi, 2), signal

    except:
        return 0, "NEUTRAL"


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

        try:
            r = requests.get(
                f"{BASE_URL}/ticker/24hr?symbol={coin}",
                timeout=10
            )

            data = r.json()

            price = float(data.get("lastPrice", 0))
            change = float(data.get("priceChangePercent", 0))

            results.append({
                "symbol": coin,
                "price": round(price, 2),
                "change": round(change, 2)
            })

        except:
            results.append({
                "symbol": coin,
                "price": 0,
                "change": 0
            })

    return results
