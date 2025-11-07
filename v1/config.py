import random
import numpy as np

class Config:
    def __init__(self, seed=0):

        # === Initialize random seeds ===
        self.seed = seed
        random.seed(self.seed)
        np.random.seed(self.seed)

        # === Vehicle Generation Settings ===
        self.vehicle_generation_interval = 10  # time steps between vehicle generations

        # === Road Configuration ===
        self.road_length = 2000          # length of the road (meters)
        self.speed_limit = 30            # speed limit (m/s)

        # === Simulation Settings ===
        self.time_max = 1000
        self.simulation_time_step = 0.1         # delta t (s)

        # === IDM ===
        self.idm_desired_speed = self.speed_limit #v_0 
        self.idm_minimum_spacing = 3          # s_0
        self.idm_safety_time_headway = 1.5    # T
        self.idm_acceleration = 2             # a
        self.idm_desired_deceleration = 3     # b
        self.idm_delay = 0.4                  # tau

        self.vehicle_length = 5               # L                
        self.initial_acceleration = 0         # initial acceleration (m/s^2)





