import random


def ai_predict(symbol):

    predictions = [
        "Bullish breakout possible",
        "Market likely sideways",
        "Possible short-term pullback",
        "Strong upward momentum forming",
        "Bearish pressure detected"
    ]

    return random.choice(predictions)


def signal_strength(rsi):

    if rsi < 30:
        return "STRONG BUY"
    elif rsi < 40:
        return "BUY"
    elif rsi < 60:
        return "NEUTRAL"
    elif rsi < 70:
        return "SELL"
    else:
        return "STRONG SELL"
