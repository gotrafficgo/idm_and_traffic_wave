import random
import numpy as np

class Config:
    def __init__(self, seed=1):
        # === Initialize random seeds ===
        self.seed = seed
        random.seed(self.seed)
        np.random.seed(self.seed)

        # === Road Configuration ===
        self.speed_limit = 30                # speed limit (m/s)
        self.road_length = 2000              # total road length (m)            

        # === Simulation Settings ===
        self.simulation_time_step = 0.1      # simulation time step Δt (s)
        self.time_max = 1000                 # total simulation time (s)               

        # === IDM Parameters ===
        self.idm_minimum_spacing = 2         # minimum spacing s0 (m) [recommended: 1.5 ~ 2.5]
        self.idm_safety_time_headway = 1     # safety time headway T (s) [recommended: 1.2 ~ 1.5]
        self.idm_acceleration = 1.5          # maximum acceleration a (m/s^2) [recommended: 1.0 ~ 1.2]
        self.idm_desired_deceleration = 2    # comfortable deceleration b (m/s^2) [recommended: 1.2 ~ 1.5]
        self.idm_delay = 0.4                 # reaction delay τ (s) [recommended: 0.5 ~ 0.6]

        self.vehicle_length = 5              # vehicle length L (m)
        self.initial_speed = self.speed_limit  # initial speed (m/s)
        self.initial_acceleration = 0          # initial acceleration (m/s^2)
        self.relative_speed_noise = 0.5        # STD of speed perception noise (m/s)

        # === Bottleneck Settings ===
        self.bottleneck_length   = 200                         # bottleneck length (m)
        self.bottleneck_x_start  = self.road_length - 500      # bottleneck start position (m)
        self.bottleneck_x_end    = self.bottleneck_x_start + self.bottleneck_length  # bottleneck end position (m)
        self.bottleneck_t_start  = 100                         # bottleneck activation time (s)        
        self.bottleneck_speed_limit = self.speed_limit * 0.2   # bottleneck speed limit (m/s)
        self.percentage_influenced_by_bottleneck = 0.7         # percentage of vehicles affected by bottleneck


        


        # === Experiment Selection ===
        # Experiemnt 1: Deterministic Inflow + Short-lasting Bottleneck 
        # Experiemnt 2: Stochastic Inflow + Short-lasting Bottleneck
        # Experiemnt 3: Deterministic Inflow + Long-lasting Bottleneck
        # Experiemnt 4: Stochastic Inflow + Long-lasting Bottleneck
        
        whichExperiment = 3  

        # === Vehicle Generation Settings ===
        # Each vehicle's inter-arrival time = minimum_interval + exponential_random_interval
        if whichExperiment == 1:
            self.vehicle_min_interval   = 2.5      # minimum generation interval t_min (s)
            self.vehicle_extra_interval = 0      # expected value of exponential interval extra_interval (s)
            self.bottleneck_t_end       = 200               # bottleneck deactivation time (s)
        
        elif whichExperiment == 2:
            self.vehicle_min_interval   = 1.5      # minimum generation interval t_min (s)
            self.vehicle_extra_interval = 1      # expected value of exponential interval extra_interval (s)        
            self.bottleneck_t_end       = 200               # bottleneck deactivation time (s)
        
        elif whichExperiment == 3:
            self.vehicle_min_interval   = 2.5      # minimum generation interval t_min (s)
            self.vehicle_extra_interval = 0      # expected value of exponential interval extra_interval (s)
            self.bottleneck_t_end       = self.time_max               # bottleneck deactivation time (s)
        
        elif whichExperiment == 4:
            self.vehicle_min_interval   = 1.5      # minimum generation interval t_min (s)
            self.vehicle_extra_interval = 1      # expected value of exponential interval extra_interval (s)        
            self.bottleneck_t_end       = self.time_max               # bottleneck deactivation time (s)


