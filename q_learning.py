import numpy as np
from sumo_environment import SumoEnvironment

# Hyperparamètres
alpha = 0.1
gamma = 0.99
epsilon = 0.1
episodes = 1000

environment = SumoEnvironment()
q_table = np.zeros([environment.observation_space.shape[0], environment.action_space.n])

for episode in range(episodes):
    state, _ = environment.reset()
    done = False

    while not done:
        if np.random.uniform(0, 1) < epsilon:
            action = environment.action_space.sample()
        else:
            action = np.argmax(q_table[state])

        next_state, reward, done, _, _ = environment.step(action)

        # Mise à jour Q-table
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state, action] = new_value

        state = next_state

environment.close()