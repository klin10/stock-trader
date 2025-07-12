import gym
import numpy as np
import pandas as pd
from gym import spaces

class StockTradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(StockTradingEnv, self).__init__()

        self.df = df
        self.reward_range = (0, np.inf)

        # Actions: 0=Sell, 1=Hold, 2=Buy
        self.action_space = spaces.Discrete(3)

        # Observations: [account_balance, shares_held, current_price] + market_data
        # The length of the observation space depends on the number of features from the dataframe
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(3 + len(df.columns),), dtype=np.float32)

        self.reset()

    def reset(self):
        self.balance = 10000  # Initial balance
        self.shares_held = 0
        self.current_step = 0
        self.net_worth = self.balance
        return self._next_observation()

    def _next_observation(self):
        obs = np.array([
            self.balance,
            self.shares_held,
            self.df.loc[self.current_step, 'close'],
        ] + self.df.loc[self.current_step].values.tolist())
        return obs

    def step(self, action):
        self.current_step += 1

        if self.current_step >= len(self.df) - 1:
            self.current_step = 0 # or handle episode end

        # Execute action
        if action == 0: # Sell
            if self.shares_held > 0:
                self.balance += self.shares_held * self.df.loc[self.current_step, 'close']
                self.shares_held = 0
        elif action == 2: # Buy
            if self.balance > self.df.loc[self.current_step, 'close']:
                self.shares_held = self.balance / self.df.loc[self.current_step, 'close']
                self.balance = 0

        # Update net worth
        self.net_worth = self.balance + self.shares_held * self.df.loc[self.current_step, 'close']

        # Calculate reward
        reward = self.net_worth - 10000 # Simple profit-based reward

        done = self.net_worth <= 0 or self.current_step >= len(self.df) -1

        obs = self._next_observation()

        return obs, reward, done, {}

    def render(self, mode='human', close=False):
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}')
        print(f'Net worth: {self.net_worth}')
