class Vehicle:

    def __init__(self, config, id, vehicle_front=None):
        self.id = id        
        self.position = 0
        self.speed = config.speed_limit
        self.speed_max = config.speed_limit
        self.vehicle_front = vehicle_front
        self.road_length = config.road_length
        
        self.history = []

         # IDM Parameters
        self.v0         = config.idm_desired_speed
        self.s0         = config.idm_minimum_spacing
        self.T          = config.idm_safety_time_headway
        self.a_max      = config.idm_acceleration
        self.b_desired  = config.idm_desired_deceleration
        self.tau        = config.idm_delay
        self.L          = config.vehicle_length
        self.delta_t    = config.simulation_time_step
        self.a          = config.initial_acceleration
        self.d          = 0 # moving distance in current step


    ##### Update-1
    def update_acceleration(self):
        ### Initalization
        if self.vehicle_front is None:
            v_front_speed  = 0 
            v_front_position = self.road_length
            # v_front_speed  = self.speed_max
            # v_front_position = self.position + 1e6  # A large distance ahead            
        else:
            v_front_speed = self.vehicle_front.speed
            v_front_position = self.vehicle_front.position

        v         = self.speed
        delta_v   = v - v_front_speed
        s         = v_front_position - self.position - self.L                
        s0        = self.s0
        a_max     = self.a_max
        b_desired = self.b_desired

        ### s_star
        term1 = self.T * v
        term2 = v * delta_v / (2 * (a_max * b_desired) ** 0.5)
        s_star = s0 + max(0, term1 + term2)

        ### acceleration update
        term1 = (v/self.v0) ** 4 # positive number
        term2 = (s_star/s) ** 2  # positive number   
        a = a_max * (1 - term1 - term2)    

        self.a = a


    ##### Update-2
    def update_speed(self):
        # Has left the road
        if self.position >= self.road_length:
            v_new = 30

        # Within the road
        else:
            ### Initalization
            a = self.a
            delta_t = self.delta_t
            v = self.speed

            ### speed update
            v_new = v + a * delta_t

        self.speed = v_new

    
    ##### Update-3
    def update_position(self):
        ### Initalization
        a = self.a
        v = self.speed
        delta_t = self.delta_t
        
        ### position update
        d = v * delta_t + 0.5 * a * delta_t ** 2

        self.d = d
        self.position = self.position + self.d

    
    def record_state(self, t):
        self.history.append({
            "t": t,
            "position": self.position,
            "speed": self.speed,
            "acceleration": self.a,
            "moving_distance": self.d
        })


