from fastapi import FastAPI
from fastapi.responses import JSONResponse
import yfinance as yf
import numpy as np

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stock API is running"}

@app.get("/analyze/{symbol}")
def analyze_stock(symbol: str):
    try:
        # Download stock data for last 30 days
        df = yf.download(symbol, period="1mo", interval="1d")

        if df.empty:
            return JSONResponse(
                status_code=404,
                content={"error": f"No data found for symbol: {symbol}"}
            )

        # Example calculation: latest close, average close, count of rows
        latest_close = df["Close"].iloc[-1]
        avg_close = df["Close"].mean()
        row_count = len(df)

        # Convert any numpy values to native Python types
        result = {
            "symbol": symbol.upper(),
            "latest_close": float(latest_close),
            "average_close": float(avg_close),
            "row_count": int(row_count)
        }

        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
