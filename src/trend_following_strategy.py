import pandas as pd
from src.strategy import Strategy

class TrendFollowingStrategy(Strategy):
    def __init__(self, short_window=5, long_window=20):
        super().__init__("Trend Following Strategy")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # Calculate short and long moving averages
        signals['short_mavg'] = df['close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = df['close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        # Buy signal: short mavg crosses above long mavg
        signals['signal'][self.short_window:] = \
            (signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:]).astype(float)

        signals['positions'] = signals['signal'].diff()
        return signals
