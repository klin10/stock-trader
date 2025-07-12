from src.rl_environment import StockTradingEnv
from src.rl_agent import DQNAgent
from src.strategy import get_data
import numpy as np

def evaluate_rl_agent(ticker, model_path):
    df = get_data(ticker)
    env = StockTradingEnv(df)
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    agent.load(model_path)
    agent.epsilon = 0.0 # Set epsilon to 0 to disable exploration

    state = env.reset()
    state = np.reshape(state, [1, state_size])
    total_reward = 0

    for _ in range(len(df)):
        action = agent.act(state)
        next_state, reward, done, _ = env.step(action)
        total_reward += reward
        next_state = np.reshape(next_state, [1, state_size])
        state = next_state
        if done:
            break

    print(f"Total reward: {total_reward}")
    return total_reward

if __name__ == '__main__':
    # Example usage
    # evaluate_rl_agent('AAPL', 'models/rl_model_AAPL_40.h5')
    pass
