from config import Config
from simulator import Simulator
from plotting import plot_time_space_diagram


def main():

    # Load simulation parameters
    config = Config()

    # Initialize simulator
    sim = Simulator(config)

    # Run the simulation loop
    sim.run()

    # Generate the time–space diagram
    plot_time_space_diagram(sim, config)


if __name__ == "__main__":
    main()