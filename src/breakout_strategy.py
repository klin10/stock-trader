import pandas as pd
from src.strategy import Strategy

class BreakoutStrategy(Strategy):
    def __init__(self, consolidation_window=20, volume_threshold=2.0):
        super().__init__("Breakout Strategy")
        self.consolidation_window = consolidation_window
        self.volume_threshold = volume_threshold

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # Calculate Bollinger Bands
        df['middle_band'] = df['close'].rolling(window=self.consolidation_window).mean()
        df['upper_band'] = df['middle_band'] + 2 * df['close'].rolling(window=self.consolidation_window).std()
        df['lower_band'] = df['middle_band'] - 2 * df['close'].rolling(window=self.consolidation_window).std()


        # Calculate average volume
        df['avg_volume'] = df['volume'].rolling(window=self.consolidation_window).mean()

        # Buy signal: price breaks above the upper band with high volume
        signals.loc[(df['close'] > df['upper_band']) & (df['volume'] > df['avg_volume'] * self.volume_threshold), 'signal'] = 1.0

        # Sell signal: price falls below the middle band
        signals.loc[df['close'] < df['middle_band'], 'signal'] = 0.0

        signals['positions'] = signals['signal'].diff()
        return signals
