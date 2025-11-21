import random
import numpy as np

class Config:
    def __init__(self, seed=1):

        # === Initialize random seeds ===
        self.seed = seed
        random.seed(self.seed)
        np.random.seed(self.seed)


        # === Vehicle Generation Settings ===
        initial_flow = 1500
        self.vehicle_generation_interval = 3600/initial_flow  # time steps between vehicle generations


        # === Road Configuration ===
        self.road_length = 2000          # length of the road (meters)
        self.speed_limit = 30            # speed limit (m/s)


        # === Simulation Settings ===
        self.time_max = 1000
        self.simulation_time_step = 0.1         # delta t (s)


        # === IDM ===
        self.idm_minimum_spacing = 2          # s_0
        self.idm_safety_time_headway = 1      # T
        self.idm_acceleration = 1.5           # a
        self.idm_desired_deceleration = 2     # b
        self.idm_delay = 0.4                  # tau

        self.vehicle_length = 5                # L                
        self.initial_speed = self.speed_limit  # initial speed (m/s)
        self.initial_acceleration = 0          # initial acceleration (m/s^2)
 
        self.relative_speed_noise = 0.5        # standard deviation of speed perception noise (m/s)


        # === Bottleneck Settings ===
        self.bottleneck_length   = 200                           # length of bottleneck (meters)
        self.bottleneck_x_start  = self.road_length - 500        # start position of bottleneck (meters)
        self.bottleneck_x_end    = self.bottleneck_x_start + self.bottleneck_length          # end position of bottleneck (meters)
        self.bottleneck_t_start  = 100            
        self.bottleneck_t_end    = 200
        self.bottleneck_speed_limit = self.speed_limit * 0.2     # speed limit in bottleneck (m/s)  





