import os
from schwab_api import Schwab
from schwab_api.enums import MarketData, Duration, Frequency
from schwab_api.models import MarketDataRequest
from dotenv import load_dotenv
from src.database import SessionLocal, StockData
from datetime import datetime

load_dotenv()

API_KEY = os.environ.get("API_KEY")
APP_SECRET = os.environ.get("APP_SECRET")
TOKEN_PATH = os.environ.get("TOKEN_PATH")

def get_schwab_client():
    return Schwab(
        app_key=API_KEY,
        app_secret=APP_SECRET,
        token_path=TOKEN_PATH
    )

def fetch_historical_data(client, ticker, start_date, end_date):
    request = MarketDataRequest(
        symbol=ticker,
        market_data_type=MarketData.MARKET_DATA,
        duration=Duration.DAY,
        frequency=Frequency.MINUTE,
        start_date=start_date,
        end_date=end_date
    )
    response = client.get_market_data(request)
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

if __name__ == "__main__":
    client = get_schwab_client()
    # Example usage
    # data = fetch_historical_data(client, "AAPL", "2023-01-01", "2023-01-31")
    # save_historical_data(data)
