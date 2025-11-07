from config import Config
from vehicle import Vehicle

class Simulator:

    def __init__(self, config: Config):
        self.config = config
        self.vehicles = []
        self.history = {
            'time': [],
            'speed': [],
            'position': [],
            'acceleration': [],
            'moving_distance': []
        }


    def run(self):
        number_of_vehicles = 0
        time_generation_last = 0

        dt = self.config.simulation_time_step  # 0.1
        num_steps = int((self.config.time_max - 1) / dt) + 1

        for i in range(num_steps):
            t = 1 + i * dt

            if abs(t % 100) < 1e-6: 
                print(f"{i} : {int(t)}")     

            if i == num_steps - 1:
                print("Simulation finished, plotting results...")        

            # Vehicle Generation
            number_of_vehicles, time_generation_last, self.vehicles = self._generate_vehicles(number_of_vehicles, t, time_generation_last, self.vehicles)
            
            # Car-following
            self._update_all_acceleration()
            self._update_all_speed() 
            self._update_all_position()

            # Record state
            self._record_all_state(t)


    def _update_all_acceleration(self):
        for vehicle in self.vehicles:
            vehicle.update_acceleration()


    def _update_all_speed(self):
        for vehicle in self.vehicles:
            vehicle.update_speed()


    def _update_all_position(self):
        for vehicle in self.vehicles:
            vehicle.update_position()


    def _record_all_state(self, t):
        for vehicle in self.vehicles:
            vehicle.record_state(t)


    def _generate_vehicles(self, number_of_vehicles, t_current, time_generation_last, vehicles):
        if vehicles:
            v_front = vehicles[-1]
        else:
            v_front = None        

        ##### Not Generating Vehicle
        # Check generation interval
        if time_generation_last > 0 and t_current - time_generation_last < self.config.vehicle_generation_interval:
            return number_of_vehicles, time_generation_last, vehicles
                
        ##### Generating Vehicle
        id = number_of_vehicles + 1      
        v = Vehicle(self.config, id, v_front)
        vehicles.append(v)

        number_of_vehicles += 1
        time_generation = t_current

        return number_of_vehicles, time_generation, vehicles

