import pandas as pd
import talib
from sqlalchemy.orm import sessionmaker
from src.database import StockData, engine

def get_data(ticker):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp)
    df = pd.read_sql(query.statement, session.bind)

    session.close()
    return df

def detect_patterns(df):
    # Example: Three Line Strike
    three_line_strike = talib.CDL3LINESTRIKE(df['open'], df['high'], df['low'], df['close'])
    df['three_line_strike'] = three_line_strike

    # Example: Evening Star
    evening_star = talib.CDLEVENINGSTAR(df['open'], df['high'], df['low'], df['close'])
    df['evening_star'] = evening_star

    return df[ (df['three_line_strike'] != 0) | (df['evening_star'] != 0) ]

def calculate_indicators(df):
    # Example: RSI
    rsi = talib.RSI(df['close'], timeperiod=14)
    df['rsi'] = rsi

    # Example: MACD
    macd, macdsignal, macdhist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['macdhist'] = macdhist

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
