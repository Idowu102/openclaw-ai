import ccxt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

exchange = ccxt.binance()

def ai_predict(symbol):

    bars = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=60)

    df = pd.DataFrame(
        bars,
        columns=["time","open","high","low","close","volume"]
    )

    X = np.array(range(len(df))).reshape(-1,1)

    y = df["close"].values

    model = LinearRegression()

    model.fit(X,y)

    future = np.array([[len(df)+1]])

    prediction = model.predict(future)[0]

    return round(float(prediction),2)


def signal_strength(rsi):

    if rsi < 25:
        return "EXTREME BUY"

    if rsi < 35:
        return "STRONG BUY"

    if rsi > 75:
        return "EXTREME SELL"

    if rsi > 65:
        return "STRONG SELL"

    return "NEUTRAL"