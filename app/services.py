import ccxt
import pandas as pd
import ta

exchange = ccxt.binance()

def get_price(symbol):

    ticker = exchange.fetch_ticker(symbol)

    return ticker["last"]


def analyze(symbol):

    bars = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=100)

    df = pd.DataFrame(
        bars,
        columns=["time","open","high","low","close","volume"]
    )

    rsi_indicator = ta.momentum.RSIIndicator(df["close"])

    df["rsi"] = rsi_indicator.rsi()

    rsi = float(df["rsi"].iloc[-1])

    if rsi < 30:
        trend = "BUY"

    elif rsi > 70:
        trend = "SELL"

    else:
        trend = "NEUTRAL"

    return round(rsi,2), trend


def scan_market():

    coins = [
        "BTC/USDT",
        "ETH/USDT",
        "SOL/USDT",
        "BNB/USDT",
        "XRP/USDT",
        "DOGE/USDT",
        "ADA/USDT",
        "AVAX/USDT",
        "MATIC/USDT"
    ]

    results = []

    for coin in coins:

        ticker = exchange.fetch_ticker(coin)

        results.append({
            "symbol": coin,
            "price": round(ticker["last"],2),
            "change": round(ticker["percentage"],2)
        })

    return results