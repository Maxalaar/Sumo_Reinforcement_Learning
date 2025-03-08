from pathlib import Path

from environment.sumo_environment import SumoEnvironment

if __name__ == "__main__":
    environment_configuration = {
        'sumo_configuration_path': Path('environment/hello/hello.sumocfg'),
        'simulation_end': 3000,
        'use_gui': False,
    }
    env = SumoEnvironment(environment_configuration)
    observation, _ = env.reset()
    for _ in range(1000):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        print("Observation:", observation, "Reward:", reward)
        if terminated or truncated:
            observation, info = env.reset()
    env.close()
