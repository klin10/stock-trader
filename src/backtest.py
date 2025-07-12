import pandas as pd
import numpy as np
from src.strategy import MovingAverageCrossover, get_data

def backtest_strategy(strategy, ticker):
    df = get_data(ticker)
    signals = strategy.generate_signals(df)

    # Combine signals with the original dataframe
    df = df.join(signals, how='inner')

    # Calculate returns
    df['returns'] = df['close'].pct_change()

    # Calculate strategy returns
    df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

    # Calculate performance metrics
    total_return = df['cumulative_returns'].iloc[-1] - 1
    sharpe_ratio = np.sqrt(252) * (df['strategy_returns'].mean() / df['strategy_returns'].std()) # Annualized

    # Get number of trades
    num_trades = len(df[df['positions'] != 0])

    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'num_trades': num_trades,
        'cumulative_returns': df['cumulative_returns']
    }


if __name__ == '__main__':
    # Example usage
    # mac = MovingAverageCrossover(short_window=10, long_window=50)
    # performance = backtest_strategy(mac, 'AAPL')
    # print(f"Total Return: {performance['total_return']:.2%}")
    # print(f"Sharpe Ratio: {performance['sharpe_ratio']:.2f}")
    # print(f"Number of Trades: {performance['num_trades']}")
    pass
