import pandas as pd
from src.data_loader import get_data


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

        signals['signal'][self.short_window:] =             (signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:]).astype(float)

        signals['positions'] = signals['signal'].diff()
        return signals



class MultiIndicatorStrategy(Strategy):
    def __init__(self, short_window=12, long_window=26, signal_window=9, rsi_period=14, rsi_overbought=70, rsi_oversold=30, bband_window=20, bband_std=2):
        super().__init__("Multi-Indicator Strategy")
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.bband_window = bband_window
        self.bband_std = bband_std

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # MACD
        exp1 = df['close'].ewm(span=self.short_window, adjust=False).mean()
        exp2 = df['close'].ewm(span=self.long_window, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macdsignal'] = df['macd'].ewm(span=self.signal_window, adjust=False).mean()
        df['macdhist'] = df['macd'] - df['macdsignal']

        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df['middle_band'] = df['close'].rolling(window=self.bband_window).mean()
        df['upper_band'] = df['middle_band'] + self.bband_std * df['close'].rolling(window=self.bband_window).std()
        df['lower_band'] = df['middle_band'] - self.bband_std * df['close'].rolling(window=self.bband_window).std()

        # Buy signals
        signals.loc[(df['macd'] > df['macdsignal']) & (df['rsi'] < self.rsi_overbought) & (df['close'] > df['lower_band']), 'signal'] = 1.0

        # Sell signals
        signals.loc[(df['macd'] < df['macdsignal']) & (df['rsi'] > self.rsi_oversold) & (df['close'] < df['upper_band']), 'signal'] = 0.0

        signals['positions'] = signals['signal'].diff()
        return signals

if __name__ == '__main__':
    from src.ichimoku_strategy import IchimokuStrategy
    # Example usage
    df = get_data('AAPL')
    # mac = MovingAverageCrossover(short_window=10, long_window=50)
    # signals = mac.generate_signals(df)
    # print(signals.tail(10))

    # mis = MultiIndicatorStrategy()
    # signals = mis.generate_signals(df.copy())
    # print(signals.tail(10))
    
    ichimoku = IchimokuStrategy()
    signals = ichimoku.generate_signals(df.copy())
    print(signals.tail(10))
