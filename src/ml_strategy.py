import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from src.strategy import Strategy, get_data
from src.technical_analysis import calculate_indicators

class MLStrategy(Strategy):
    def __init__(self, model):
        super().__init__("Machine Learning Strategy")
        self.model = model

    def generate_signals(self, df):
        # This is a simplified approach. In a real-world scenario, you would
        # want to be more careful about lookahead bias.
        features = self.create_features(df)

        # Drop rows with NaN values
        features = features.dropna()

        if features.empty:
            return pd.DataFrame(index=df.index)

        predictions = self.model.predict(features)

        signals = pd.DataFrame(index=features.index)
        signals['signal'] = predictions
        signals['positions'] = signals['signal'].diff()

        return signals

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

def train_model(ticker):
    df = get_data(ticker)

    # Create features and target
    mls = MLStrategy(None) # Temporary instance
    features = mls.create_features(df)

    # Create target variable (1 if next day's price goes up, 0 otherwise)
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    # Align features and target
    data = features.join(df['target'], how='inner').dropna()

    X = data.drop('target', axis=1)
    y = data['target']

    if len(X) == 0:
        print("Not enough data to train the model.")
        return None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    return model


if __name__ == '__main__':
    # Example usage
    # model = train_model('AAPL')
    # if model:
    #     mls = MLStrategy(model)
    #     df = get_data('AAPL')
    #     signals = mls.generate_signals(df)
    #     print(signals.tail(10))
    pass
