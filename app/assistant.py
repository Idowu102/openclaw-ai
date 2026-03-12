def ai_assistant(symbol, signal, prediction):

    if signal == "BUY":
        return f"AI analysis: {symbol} shows bullish momentum toward {prediction}"

    if signal == "SELL":
        return f"AI warning: {symbol} may correct after being overbought."

    return f"AI view: {symbol} is consolidating. Wait for breakout."