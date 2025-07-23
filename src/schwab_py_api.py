import os
import asyncio
from schwab_py import Schwab
from schwab_py.utils import get_current_datetime
from schwab_py.enum import MarketHours, Projection, Entitlement
from dotenv import load_dotenv
from src.database import SessionLocal, StockData
from datetime import datetime

load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_SECRET = os.environ.get("APP_SECRET")
TOKEN_PATH = os.environ.get("TOKEN_PATH")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

async def get_schwab_client():
    # schwab-py uses an async model, so we'll use an async function
    s = Schwab()
    await s.load_key_from_path(TOKEN_PATH)
    # The library handles token refresh automatically
    return s

async def fetch_historical_data(client, ticker, start_date, end_date):
    response = await client.get_price_history(
        symbol=ticker,
        start_date=start_date,
        end_date=end_date,
        frequency_type='minute',
        frequency=1,
        extended_hours=False
    )
    return response.json()

def save_historical_data(data):
    db = SessionLocal()
    for item in data["candles"]:
        stock_data = StockData(
            ticker=data["symbol"],
            timestamp=datetime.fromtimestamp(item["datetime"] / 1000),
            open=item["open"],
            high=item["high"],
            low=item["low"],
            close=item["close"],
            volume=item["volume"]
        )
        db.add(stock_data)
    db.commit()
    db.close()

async def main():
    # To run this async script directly
    client = await get_schwab_client()
    # Example usage
    # start = get_current_datetime().replace(day=1, month=1, year=2023)
    # end = get_current_datetime().replace(day=31, month=1, year=2023)
    # data = await fetch_historical_data(client, "AAPL", start, end)
    # save_historical_data(data)

if __name__ == "__main__":
    asyncio.run(main())
