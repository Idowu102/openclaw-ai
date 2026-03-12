import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

BASE_URL = "https://api.binance.com/api/v3"


def ai_predict(symbol):

    pair = symbol.upper()

    try:
        r = requests.get(
            f"{BASE_URL}/klines?symbol={pair}&interval=1m&limit=60",
            timeout=10
        )

        data = r.json()

        closes = [float(x[4]) for x in data]

        df = pd.DataFrame(closes, columns=["close"])

        X = np.array(range(len(df))).reshape(-1, 1)

        y = df["close"].values

        model = LinearRegression()

        model.fit(X, y)

        future = np.array([[len(df) + 1]])

        prediction = model.predict(future)[0]

        return round(float(prediction), 2)

    except:
        return 0


def signal_strength(rsi):

    if rsi < 25:
        return "EXTREME BUY"

    elif rsi < 35:
        return "STRONG BUY"

    elif rsi > 75:
        return "EXTREME SELL"

    elif rsi > 65:
        return "STRONG SELL"

    else:
        return "NEUTRAL"
