import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import StockData, engine

def detect_abnormal_moves(ticker, window=10, volume_threshold=2.0, price_change_threshold=2.0):
    """
    Detects abnormal moves for a given ticker by analyzing recent data.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch the last 'window' minutes of data
    query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp.desc()).limit(window)
    df = pd.read_sql(query.statement, session.bind)
    df = df.sort_values(by='timestamp').reset_index(drop=True)

    if len(df) < 2:
        return pd.DataFrame()

    df['price_delta'] = df['close'].diff()
    df['volume_delta'] = df['volume'].diff()

    # Calculate rolling averages and standard deviations
    df['rolling_avg_price_delta'] = df['price_delta'].abs().rolling(window=window, min_periods=1).mean()
    df['rolling_std_price_delta'] = df['price_delta'].abs().rolling(window=window, min_periods=1).std()
    df['rolling_avg_volume'] = df['volume'].rolling(window=window, min_periods=1).mean()
    df['rolling_std_volume'] = df['volume'].rolling(window=window, min_periods=1).std()

    # Identify abnormal moves
    price_z_score = (df['price_delta'].abs() - df['rolling_avg_price_delta']) / df['rolling_std_price_delta']
    volume_z_score = (df['volume'] - df['rolling_avg_volume']) / df['rolling_std_volume']

    abnormal_price = df[price_z_score > price_change_threshold]
    abnormal_volume = df[volume_z_score > volume_threshold]

    abnormal_moves = pd.concat([abnormal_price, abnormal_volume]).drop_duplicates()

    session.close()

    return abnormal_moves

def notify_abnormal_moves(moves):
    """
    Placeholder for a notification system.
    """
    for _, row in moves.iterrows():
        print(f"ALERT: Abnormal move for {row['ticker']} at {row['timestamp']}")
        print(f"  Price: {row['close']:.2f}, Price Delta: {row['price_delta']:.2f}")
        print(f"  Volume: {row['volume']}")

if __name__ == '__main__':
    # This is an example of how you might use this in a streaming context
    # In a real application, you would call this function periodically
    # with the latest data.
    # For demonstration, we'll just run it once on the existing data.

    # abnormal_moves = detect_abnormal_moves('AAPL')
    # if not abnormal_moves.empty:
    #     notify_abnormal_moves(abnormal_moves)
    pass
