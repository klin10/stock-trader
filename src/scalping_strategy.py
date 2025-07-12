import pandas as pd
from src.strategy import Strategy

class ScalpingStrategy(Strategy):
    def __init__(self, short_window=3, profit_target=0.005, stop_loss=0.002):
        super().__init__("Scalping Strategy")
        self.short_window = short_window
        self.profit_target = profit_target
        self.stop_loss = stop_loss

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # Use a very short moving average to detect small trends
        signals['short_mavg'] = df['close'].rolling(window=self.short_window, min_periods=1, center=False).mean()

        # Entry condition
        signals['entry'] = (df['close'] > signals['short_mavg'])

        # This is a simplified representation. A real scalping strategy would
        # need to manage positions and exits on a tick-by-tick basis, which
        # is difficult to simulate in a vectorized backtest.
        # We will generate a position signal and assume it's held for a very short time.

        # We'll generate a buy signal when the price crosses above the short moving average
        signals['signal'] = (df['close'] > signals['short_mavg']).astype(float)

        signals['positions'] = signals['signal'].diff()

        # In a real implementation, you would have logic to exit the position
        # based on the profit target or stop loss. This is a simplified example.

        return signals
