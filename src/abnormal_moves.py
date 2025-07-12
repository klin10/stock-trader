import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import StockData, engine

def detect_abnormal_moves(ticker, volume_threshold=2.0, price_change_threshold=2.0):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp)
    df = pd.read_sql(query.statement, session.bind)

    df['price_change'] = df['close'].diff()
    df['volume_change'] = df['volume'].diff()

    avg_volume = df['volume'].mean()
    avg_price_change = df['price_change'].abs().mean()

    abnormal_volume = df[df['volume'] > avg_volume * volume_threshold]
    abnormal_price_change = df[df['price_change'].abs() > avg_price_change * price_change_threshold]

    abnormal_moves = pd.concat([abnormal_volume, abnormal_price_change]).drop_duplicates()

    session.close()

    return abnormal_moves

def notify_abnormal_moves(moves):
    # This is a placeholder for a notification system.
    # You could implement email, SMS, or other notification methods here.
    for index, row in moves.iterrows():
        print(f"Abnormal move detected for {row['ticker']} at {row['timestamp']}:")
        print(f"  Volume: {row['volume']}")
        print(f"  Price Change: {row['price_change']}")


if __name__ == '__main__':
    # Example usage
    # abnormal_moves = detect_abnormal_moves('AAPL')
    # if not abnormal_moves.empty:
    #     notify_abnormal_moves(abnormal_moves)
    pass
