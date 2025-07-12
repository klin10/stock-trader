import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import StockData, engine

def resample_data(ticker, interval):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp)
    df = pd.read_sql(query.statement, session.bind)

    df.set_index('timestamp', inplace=True)

    resampled_df = df['close'].resample(interval).ohlc()
    resampled_df['volume'] = df['volume'].resample(interval).sum()

    session.close()

    return resampled_df

if __name__ == '__main__':
    # Example usage
    # resampled_data = resample_data('AAPL', '10Min')
    # print(resampled_data)
    pass
