from src.rl_environment import StockTradingEnv
from src.rl_agent import DQNAgent
from src.strategy import get_data

def train_rl_agent(ticker, episodes=100):
    df = get_data(ticker)
    env = StockTradingEnv(df)
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    batch_size = 32

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(len(df)):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e+1}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        if e % 10 == 0:
            agent.save(f"models/rl_model_{ticker}_{e}.h5")

if __name__ == '__main__':
    # Example usage
    # train_rl_agent('AAPL', episodes=50)
    pass
