import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import StockData, engine

def get_data(ticker):
    """
    Fetches historical stock data for a given ticker from the database.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp)
        df = pd.read_sql(query.statement, session.bind)
        if 'timestamp' in df.columns:
            df.set_index('timestamp', inplace=True)
        return df
    finally:
        session.close()
