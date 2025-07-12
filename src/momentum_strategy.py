import pandas as pd
from src.strategy import Strategy

class MomentumStrategy(Strategy):
    def __init__(self, price_momentum_window=10, volume_momentum_window=10):
        super().__init__("Momentum Strategy")
        self.price_momentum_window = price_momentum_window
        self.volume_momentum_window = volume_momentum_window

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # Calculate price and volume momentum
        df['price_momentum'] = df['close'].pct_change(self.price_momentum_window)
        df['volume_momentum'] = df['volume'].pct_change(self.volume_momentum_window)

        # Buy signal: strong positive price and volume momentum
        signals.loc[(df['price_momentum'] > 0.05) & (df['volume_momentum'] > 0.5), 'signal'] = 1.0

        # Sell signal: momentum fading
        signals.loc[(df['price_momentum'] < 0) | (df['volume_momentum'] < 0), 'signal'] = 0.0

        signals['positions'] = signals['signal'].diff()
        return signals
