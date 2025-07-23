import pandas as pd
import numpy as np
from src.strategy import MovingAverageCrossover
from src.data_loader import get_data

def backtest_strategy(strategy, df, commission_rate=0.001, annualizing_factor=252):
    signals = strategy.generate_signals(df.copy())

    # Combine signals with the original dataframe
    df = df.join(signals, how='inner')

    # Calculate returns
    df['returns'] = df['close'].pct_change()

    # Calculate strategy returns
    df['strategy_returns'] = df['returns'] * df['signal'].shift(1)

    # Apply commissions
    trades = df['positions'].abs()
    df['strategy_returns'] -= trades * commission_rate

    # Calculate cumulative returns
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

    # Calculate performance metrics
    total_return = df['cumulative_returns'].iloc[-1] - 1
    sharpe_ratio = np.sqrt(annualizing_factor) * (df['strategy_returns'].mean() / df['strategy_returns'].std()) # Annualized

    # Get number of trades
    num_trades = len(df[df['positions'] != 0])

    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'num_trades': num_trades,
        'cumulative_returns': df['cumulative_returns']
    }


from src.strategy import MultiIndicatorStrategy
from src.ml_strategy import MLStrategy

def compare_strategies(strategies, tickers, commission_rate=0.001, annualizing_factor=252):
    results = []
    for ticker in tickers:
        print(f"\n--- {ticker} ---")
        df = get_data(ticker)
        if df.empty:
            print(f"Could not get data for {ticker}")
            continue
        for strategy in strategies:
            performance = backtest_strategy(strategy, df, commission_rate, annualizing_factor)
            results.append({
                'ticker': ticker,
                'strategy': strategy.name,
                'total_return': performance['total_return'],
                'sharpe_ratio': performance['sharpe_ratio'],
                'num_trades': performance['num_trades']
            })




    results_df = pd.DataFrame(results)
    print("\n--- Strategy Comparison ---")
    print(results_df)



from src.momentum_strategy import MomentumStrategy
from src.breakout_strategy import BreakoutStrategy
from src.trend_following_strategy import TrendFollowingStrategy
from src.news_trading_strategy import NewsTradingStrategy
from src.scalping_strategy import ScalpingStrategy
from src.mean_reversion_strategy import MeanReversionStrategy

if __name__ == '__main__':
    # Example usage
    mac = MovingAverageCrossover(short_window=10, long_window=50)
    mis = MultiIndicatorStrategy()
    mls = MLStrategy()
    mom = MomentumStrategy()
    brk = BreakoutStrategy()
    tfs = TrendFollowingStrategy()
    nts = NewsTradingStrategy()
    scl = ScalpingStrategy()
    mrs = MeanReversionStrategy()


    strategies_to_compare = [mac, mis, mls, mom, brk, tfs, nts, scl, mrs]
    tickers_to_compare = ['AAPL', 'GOOG'] # Add more tickers as needed

    compare_strategies(strategies_to_compare, tickers_to_compare)
    pass
