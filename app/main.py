from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .services import get_price, analyze, scan_market
from .ai_engine import ai_predict, signal_strength
from .assistant import ai_assistant
from .portfolio import get_portfolio
from .pnl import calculate_pnl
from .trading_bot import run_bot

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if username == "admin" and password == "admin123":

        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "portfolio": get_portfolio(),
                "scanner": scan_market()
            }
        )

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid login"}
    )


@app.post("/analyze", response_class=HTMLResponse)
def analyze_market(
    request: Request,
    symbol: str = Form(...),
    capital: float = Form(100),
    entry: float = Form(0),
    size: float = Form(1)
):

    price = get_price(symbol)

    rsi, trend = analyze(symbol)

    prediction = ai_predict(symbol)

    strength = signal_strength(rsi)

    risk = round(capital * 0.02, 2)

    assistant = ai_assistant(symbol, trend, prediction)

    pnl, percent = calculate_pnl(entry, price, size)

    bot = run_bot(symbol)

    tv_symbol = "BINANCE:" + symbol.replace("/", "")

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "symbol": symbol,
            "tv_symbol": tv_symbol,
            "price": price,
            "rsi": rsi,
            "trend": trend,
            "prediction": prediction,
            "strength": strength,
            "risk": risk,
            "assistant": assistant,
            "pnl": pnl,
            "percent": percent,
            "bot": bot,
            "portfolio": get_portfolio(),
            "scanner": scan_market()
        }
    )