from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import ta

app = FastAPI()

@app.get("/analyze/{symbol}")
def analyze_stock(symbol: str):
    ticker = f"{symbol}.NS"
    stock = yf.Ticker(ticker)
    data = stock.history(period="365d")

    if data.empty:
        return {"error": "No data found. Check symbol or internet."}

    # RSI
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    latest_rsi = data['RSI'].iloc[-1]

    # Moving Averages
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    sma_50 = data['SMA_50'].iloc[-1]
    sma_200 = data['SMA_200'].iloc[-1]

    # Support
    support = data['Close'].rolling(window=20).min().iloc[-1]

    # Today return
    today_return = data['Close'].pct_change().iloc[-1]

    # Current price
    current_price = data['Close'].iloc[-1]

    # Buy signal calculation
    buy_signals = 0
    buy_signals += latest_rsi < 30
    buy_signals += sma_50 > sma_200
    buy_signals += current_price <= support * 1.05
    buy_signals += today_return > 0

    verdict = "BUY" if buy_signals >= 3 else "NOT_BUY"

    return {
        "symbol": symbol,
        "current_price": round(current_price, 2),
        "RSI": round(latest_rsi, 2),
        "SMA_50": round(sma_50, 2),
        "SMA_200": round(sma_200, 2),
        "support": round(support, 2),
        "today_return": round(today_return * 100, 2),
        "buy_signals": buy_signals,
        "verdict": verdict
    }
