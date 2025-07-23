import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import StockData, engine

def get_data(ticker):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp)
    df = pd.read_sql(query.statement, session.bind)

    session.close()
    return df

def is_three_line_strike(df: pd.DataFrame, index: int) -> int:
    """
    Identifies the Three Line Strike pattern.

    Args:
        df: DataFrame with 'Open', 'High', 'Low', 'Close' columns.
        index: The current index to check.

    Returns:
        1 for a bullish Three Line Strike, -1 for a bearish Three Line Strike, 0 otherwise.
    """
    if index < 3:
        return 0

    # Bullish Three Line Strike
    is_bullish_candle1 = df['close'][index - 3] > df['open'][index - 3]
    is_bullish_candle2 = df['close'][index - 2] > df['open'][index - 2]
    is_bullish_candle3 = df['close'][index - 1] > df['open'][index - 1]
    is_bearish_candle4 = df['close'][index] < df['open'][index]

    if (is_bullish_candle1 and is_bullish_candle2 and is_bullish_candle3 and is_bearish_candle4 and
            df['close'][index - 2] > df['close'][index - 3] and
            df['close'][index - 1] > df['close'][index - 2] and
            df['open'][index] > df['close'][index - 1] and
            df['close'][index] < df['open'][index - 3]):
        return 1

    # Bearish Three Line Strike
    is_bearish_candle1 = df['close'][index - 3] < df['open'][index - 3]
    is_bearish_candle2 = df['close'][index - 2] < df['open'][index - 2]
    is_bearish_candle3 = df['close'][index - 1] < df['open'][index - 1]
    is_bullish_candle4 = df['close'][index] > df['open'][index]

    if (is_bearish_candle1 and is_bearish_candle2 and is_bearish_candle3 and is_bullish_candle4 and
            df['close'][index - 2] < df['close'][index - 3] and
            df['close'][index - 1] < df['close'][index - 2] and
            df['open'][index] < df['close'][index - 1] and
            df['close'][index] > df['open'][index - 3]):
        return -1

    return 0

def is_evening_star(df: pd.DataFrame, index: int) -> int:
    """
    Identifies the Evening Star pattern.

    Args:
        df: DataFrame with 'Open', 'High', 'Low', 'Close' columns.
        index: The current index to check.

    Returns:
        -1 for an Evening Star, 0 otherwise.
    """
    if index < 2:
        return 0

    first_candle_is_bullish = df['close'][index - 2] > df['open'][index - 2]
    third_candle_is_bearish = df['close'][index] < df['open'][index]

    # Check for the gap up for the second candle
    gap_up = df['open'][index - 1] > df['close'][index - 2]

    # Check that the third candle closes well into the first candle's body
    reversal = df['close'][index] < (df['open'][index - 2] + (df['close'][index - 2] - df['open'][index - 2]) / 2)

    if first_candle_is_bullish and third_candle_is_bearish and gap_up and reversal:
        return -1
    return 0

def detect_patterns(df):
    # Example: Three Line Strike
    df['three_line_strike'] = [is_three_line_strike(df, i) for i in range(len(df))]
    
    # Example: Evening Star
    df['evening_star'] = [is_evening_star(df, i) for i in range(len(df))]

    return df[ (df['three_line_strike'] != 0) | (df['evening_star'] != 0) ]

def calculate_indicators(df):
    # Example: RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Example: MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['macdsignal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macdhist'] = df['macd'] - df['macdsignal']

    return df

if __name__ == '__main__':
    # Example usage
    # df = get_data('AAPL')
    # df_with_indicators = calculate_indicators(df)
    # df_with_patterns = detect_patterns(df_with_indicators)
    # print("Indicators:")
    # print(df_with_indicators.tail())
    # print("\nPatterns:")
    # print(df_with_patterns)
    pass
