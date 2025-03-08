from pathlib import Path
import gymnasium as gym
from gymnasium import spaces
import traci
import sumolib
import numpy as np


class SumoEnvironment(gym.Env):
    def __init__(self, environment_configuration=None):
        super().__init__()

        # Configuration SUMO
        if environment_configuration is None:
            environment_configuration = {}
        self.sumo_config = {
            "sumocfg_file": environment_configuration.get('sumo_configuration_path', Path('environment/hello/hello.sumocfg')),
            "simulation_end": environment_configuration.get('simulation_end', 1000),
            "gui": environment_configuration.get('use_gui', False),
        }

        # Définition de l'espace d'observation (exemple : [position, vitesse])
        self.observation_space = spaces.Box(low=0, high=1000, shape=(2,), dtype=np.float32)
        # Définition de l'espace d'action (0: accélérer, 1: maintenir, 2: ralentir)
        self.action_space = spaces.Discrete(3)

        self.sumo_cmd = None
        self.sumo = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Choisir le binaire SUMO
        sumo_binary = sumolib.checkBinary('sumo' if not self.sumo_config["gui"] else 'sumo-gui')
        # Préparer la commande en utilisant le fichier simple.sumocfg
        self.sumo_cmd = [
            sumo_binary,
            "-c", self.sumo_config["sumocfg_file"],
            "--quit-on-end", "1"
        ]
        traci.start(self.sumo_cmd)
        self.sumo = traci

        return self._get_observation(), {}

    def step(self, action):
        # Récupérer la vitesse actuelle du véhicule "veh0"
        speed = self.sumo.vehicle.getSpeed("veh0")
        if action == 0:  # Accélérer
            self.sumo.vehicle.setSpeed("veh0", speed + 1)
        elif action == 2:  # Ralentir
            self.sumo.vehicle.setSpeed("veh0", max(0, speed - 1))
        # Si action == 1, maintenir la vitesse

        self.sumo.simulationStep()

        reward = self._calculate_reward()
        terminated = self.sumo.simulation.getTime() >= self.sumo_config["simulation_end"]
        truncated = False

        return self._get_observation(), reward, terminated, truncated, {}

    def _get_observation(self):
        # Exemple d'observation : position x et vitesse du véhicule "veh0"
        pos = self.sumo.vehicle.getPosition("veh0")[0]
        speed = self.sumo.vehicle.getSpeed("veh0")
        return np.array([pos, speed], dtype=np.float32)

    def _calculate_reward(self):
        # Exemple : récompense égale à la vitesse actuelle
        return self.sumo.vehicle.getSpeed("veh0")

    def close(self):
        if self.sumo:
            self.sumo.close()