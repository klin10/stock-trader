import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.strategy import Strategy
from src.technical_analysis import calculate_indicators

class MLStrategy(Strategy):
    def __init__(self, training_window=100):
        super().__init__("Machine Learning Strategy")
        self.training_window = training_window
        self.model = LogisticRegression()

    def generate_signals(self, df):
        features = self.create_features(df)
        
        # Create target variable
        df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

        # Align features and target
        data = features.join(df['target'], how='inner').dropna()
        
        X = data.drop('target', axis=1)
        y = data['target']

        signals = pd.DataFrame(index=df.index)
        signals['signal'] = 0.0
        
        if len(X) < self.training_window:
            print("Not enough data to generate signals.")
            return signals

        predictions = []
        for i in range(self.training_window, len(X)):
            X_train = X.iloc[i-self.training_window:i]
            y_train = y.iloc[i-self.training_window:i]
            
            self.model.fit(X_train, y_train)
            
            prediction = self.model.predict(X.iloc[i:i+1])
            predictions.append(prediction[0])

        # Align predictions with the original dataframe index
        prediction_series = pd.Series(predictions, index=X.index[self.training_window:])
        signals['signal'] = prediction_series

        signals['positions'] = signals['signal'].diff()
        return signals.fillna(0)

    def create_features(self, df):
        # Use existing function to calculate indicators
        df_with_indicators = calculate_indicators(df.copy())

        # Add more features
        df_with_indicators['price_change'] = df_with_indicators['close'].diff()
        df_with_indicators['volume_change'] = df_with_indicators['volume'].diff()

        # Add lagged returns
        for i in range(1, 6):
            df_with_indicators[f'lag_return_{i}'] = df_with_indicators['close'].pct_change(i)

        # Add volatility
        df_with_indicators['volatility'] = df_with_indicators['close'].rolling(window=10).std()

        # Select features
        features = df_with_indicators[['rsi', 'macd', 'macdsignal', 'macdhist', 'price_change', 'volume_change', 'volatility'] + [f'lag_return_{i}' for i in range(1, 6)]]

        return features.dropna()
