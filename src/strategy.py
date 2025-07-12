import pandas as pd
from src.database import StockData, engine
from sqlalchemy.orm import sessionmaker

class Strategy:
    def __init__(self, name):
        self.name = name

    def generate_signals(self, df):
        raise NotImplementedError

class MovingAverageCrossover(Strategy):
    def __init__(self, short_window, long_window):
        super().__init__("Moving Average Crossover")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        signals['short_mavg'] = df['close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = df['close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        signals['signal'][self.short_window:] = \
            (signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:]).astype(float)

        signals['positions'] = signals['signal'].diff()
        return signals

def get_data(ticker):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.timestamp)
    df = pd.read_sql(query.statement, session.bind)
    df.set_index('timestamp', inplace=True)
    session.close()
    return df

if __name__ == '__main__':
    # Example usage
    # df = get_data('AAPL')
    # mac = MovingAverageCrossover(short_window=10, long_window=50)
    # signals = mac.generate_signals(df)
    # print(signals.tail(10))
    pass
