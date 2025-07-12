import pandas as pd
import talib
from src.strategy import Strategy

class MeanReversionStrategy(Strategy):
    def __init__(self, window=20, std_dev=2):
        super().__init__("Mean Reversion Strategy")
        self.window = window
        self.std_dev = std_dev

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # Calculate Bollinger Bands
        df['upper_band'], df['middle_band'], df['lower_band'] = talib.BBANDS(df['close'], timeperiod=self.window, nbdevup=self.std_dev, nbdevdn=self.std_dev)

        # Buy signal: price touches the lower band
        signals.loc[df['close'] < df['lower_band'], 'signal'] = 1.0

        # Sell signal: price touches the upper band
        signals.loc[df['close'] > df['upper_band'], 'signal'] = 0.0

        signals['positions'] = signals['signal'].diff()
        return signals
