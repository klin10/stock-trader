
import pandas as pd
from src.strategy import Strategy

class IchimokuStrategy(Strategy):
    def __init__(self, tenkan_period=9, kijun_period=26, senkou_span_b_period=52, chikou_period=26, senkou_shift=26):
        super().__init__("Ichimoku Cloud Strategy")
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_span_b_period = senkou_span_b_period
        self.chikou_period = chikou_period
        self.senkou_shift = senkou_shift

    def generate_signals(self, df):
        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0

        # Tenkan-sen (Conversion Line)
        tenkan_sen_high = df['high'].rolling(window=self.tenkan_period).max()
        tenkan_sen_low = df['low'].rolling(window=self.tenkan_period).min()
        df['tenkan_sen'] = (tenkan_sen_high + tenkan_sen_low) / 2

        # Kijun-sen (Base Line)
        kijun_sen_high = df['high'].rolling(window=self.kijun_period).max()
        kijun_sen_low = df['low'].rolling(window=self.kijun_period).min()
        df['kijun_sen'] = (kijun_sen_high + kijun_sen_low) / 2

        # Senkou Span A (Leading Span A)
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(self.senkou_shift)

        # Senkou Span B (Leading Span B)
        senkou_span_b_high = df['high'].rolling(window=self.senkou_span_b_period).max()
        senkou_span_b_low = df['low'].rolling(window=self.senkou_span_b_period).min()
        df['senkou_span_b'] = ((senkou_span_b_high + senkou_span_b_low) / 2).shift(self.senkou_shift)

        # Chikou Span (Lagging Span)
        df['chikou_span'] = df['close'].shift(-self.chikou_period)

        # Signals
        # Bullish signal
        buy_conditions = (
            (df['close'] > df['senkou_span_a']) &
            (df['close'] > df['senkou_span_b']) &
            (df['tenkan_sen'] > df['kijun_sen']) &
            (df['chikou_span'] > df['close'].shift(-self.chikou_period))
        )
        signals.loc[buy_conditions, 'signal'] = 1.0

        # Bearish signal
        sell_conditions = (
            (df['close'] < df['senkou_span_a']) &
            (df['close'] < df['senkou_span_b']) &
            (df['tenkan_sen'] < df['kijun_sen']) &
            (df['chikou_span'] < df['close'].shift(-self.chikou_period))
        )
        signals.loc[sell_conditions, 'signal'] = -1.0
        
        signals['positions'] = signals['signal'].diff()
        return signals
