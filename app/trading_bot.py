from .services import analyze, get_price

def run_bot(symbol):

    price = get_price(symbol)

    rsi, signal = analyze(symbol)

    if signal == "BUY":
        return f"BOT SIGNAL: BUY {symbol} near {price}"

    if signal == "SELL":
        return f"BOT SIGNAL: SELL {symbol} near {price}"

    return "BOT SIGNAL: HOLD"