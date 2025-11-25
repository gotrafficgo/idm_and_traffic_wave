import random

class Vehicle:

    def __init__(self, config, id, vehicle_front=None):
        self.id = id        
        self.position = 0
        self.vehicle_front = vehicle_front

        # Road and vehicle initialization
        self.road_length = config.road_length
        self.speed_limit = config.speed_limit
        self.speed       = config.initial_speed
        self.history     = []

        # Bottleneck parameters
        self.bottleneck_x_start     = config.bottleneck_x_start
        self.bottleneck_x_end       = config.bottleneck_x_end
        self.bottleneck_t_start     = config.bottleneck_t_start
        self.bottleneck_t_end       = config.bottleneck_t_end
        self.bottleneck_speed_limit = config.bottleneck_speed_limit        

        # IDM parameters
        self.v0         = self.speed
        self.s0         = config.idm_minimum_spacing
        self.T          = config.idm_safety_time_headway
        self.a_max      = config.idm_acceleration
        self.b_desired  = config.idm_desired_deceleration
        self.tau        = config.idm_delay
        self.L          = config.vehicle_length
        self.delta_t    = config.simulation_time_step
        self.a          = config.initial_acceleration

        # Noise in relative speed perception
        self.relative_speed_noise = config.relative_speed_noise

        # Whether this vehicle reacts to bottleneck limits
        if random.random() < config.percentage_influenced_by_bottleneck:
            self.influenced_by_bottleneck = True
        else: 
            self.influenced_by_bottleneck = False


    def check_road(self, current_time):
        """Apply bottleneck speed limit if vehicle is inside spatial and temporal bottleneck."""
        if not self.influenced_by_bottleneck:
            return
        
        in_x_range = (self.position >= self.bottleneck_x_start and 
                      self.position <= self.bottleneck_x_end)
        in_t_range = (current_time >= self.bottleneck_t_start and
                      current_time <= self.bottleneck_t_end)

        if in_x_range and in_t_range:
            self.v0 = self.bottleneck_speed_limit
        else:
            self.v0 = self.speed_limit



    # ===== Update-1: Acceleration =====
    def update_acceleration(self):
        """Compute IDM acceleration with additional constraints."""

        # Handle case with no front vehicle
        if self.vehicle_front is None:
            v_front_speed    = self.speed_limit
            v_front_position = self.position + 1e6  # effectively infinite headway
        else:
            v_front_speed    = self.vehicle_front.speed
            v_front_position = self.vehicle_front.position

        v = self.speed
        v_delta = v - v_front_speed  # relative speed
        v_delta_perceived = self._perceptive_relative_speed(v_delta)

        # Net distance gap
        s = v_front_position - self.position - self.L
        s = max(s, 0.1)  # [additional constraint]

        # IDM parameters
        s0 = self.s0
        a_max = self.a_max
        b_desired = self.b_desired

        # Desired dynamical gap s*
        term1 = self.T * v
        term2 = v * v_delta_perceived / (2 * (a_max * b_desired) ** 0.5)
        s_star = s0 + max(0, term1 + term2)

        # IDM acceleration formula
        term1 = (v / self.v0) ** 4
        term2 = (s_star / s) ** 2
        a = a_max * (1 - term1 - term2)

        # [additional constraint]
        if a < -b_desired:
            a = -b_desired
        if a > a_max:
            a = a_max

        self.a = a
        


    def update_speed(self):
        """Update vehicle speed using IDM acceleration and additional safety constraints."""
        
        # Vehicle has left the road
        if self.position >= self.road_length:
            v_new = 30
        else:
            a = self.a
            v = self.speed
            delta_t = self.delta_t

            # Standard Euler update
            v_new = v + a * delta_t

            # Additional constraint: do not exceed max speed allowed by gap
            if self.vehicle_front is not None:
                s = self.vehicle_front.position - self.position - self.L
                s = max(s, 0.01)  # [additional constraint]
                v_max_allowed = s / delta_t
                v_new = min(v_new, v_max_allowed)

            # Prevent negative speeds
            v_new = max(v_new, 0)  # [additional constraint]

        self.speed = v_new  


    # ===== Update-3: Position =====
    def update_position(self):
        """Update vehicle position with kinematic equation and constraints."""
        v = self.speed
        a = self.a
        delta_t = self.delta_t

        # d = v*dt + 0.5*a*dt^2
        d = v * delta_t + 0.5 * a * delta_t ** 2
        d = max(d, 0)   # [additional constraint]

        self.position = self.position + d



    def record_state(self, t):
        """Store vehicle state for later analysis."""
        self.history.append({
            "t": t,
            "position": self.position,
            "speed": self.speed,
            "acceleration": self.a
        })


    def _perceptive_relative_speed(self, v_delta):
        """Add noise to perceived relative speed."""
        noise = random.gauss(0, self.relative_speed_noise)
        return v_delta + noise