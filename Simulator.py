from Modules.Router import *
from Modules.Clock import *
from Modules.Buffer import *
from Modules.Xbar import *
from Modules.SwitchAllocator import *
from Modules.Parser import *
from Modules.Logger import *
from Modules.Plotter import *
from operator import itemgetter
from itertools import groupby
import numpy as np


def check_valid(row, column):
    if row < 0 or row > 2 or column < 0 or column > 2:
        return False
    return True


def generate_values(mean, seed, num_values):
    np.random.seed(seed)
    values = []
    sigma = mean * 0.1

    while len(values) < num_values:
        # Generate random value
        random_value = np.random.normal(mean, sigma)

        # Check if the value is within the range of mean ± 3σ
        if mean - 3 * sigma <= random_value <= mean + 3 * sigma:
            values.append(random_value)

    return values


def initialize(routing_algo, clock_period, buffer_delay, sa_delay, xbar_delay):
    for i in range(3):
        this_row = []
        for j in range(3):
            this_row.append(
                Router(i * 3 + j, routing_algo, global_logger, global_plotter)
            )
        Router_simulate_bed.append(this_row)

    for i in range(3):
        for j in range(3):
            Router_simulate_bed[i][j].set_router_neighbours(
                Router_simulate_bed[i - 1][j] if check_valid(i - 1, j) else None,
                Router_simulate_bed[i + 1][j] if check_valid(i + 1, j) else None,
                Router_simulate_bed[i][j + 1] if check_valid(i, j + 1) else None,
                Router_simulate_bed[i][j - 1] if check_valid(i, j - 1) else None,
            )
            Router_simulate_bed[i][j].create_Xbar()

    for i in range(3):
        for j in range(3):
            Router_simulate_bed[i][j].buffer.set_delay(buffer_delay[i * 3 + j])
            Router_simulate_bed[i][j].Xbar.set_delay(xbar_delay[i * 3 + j])
            Router_simulate_bed[i][j].SwitchAllocator.set_delay(sa_delay[i * 3 + j])
            Router_simulate_bed[i][j].reporter.set_delay(clock_period)

    global_plotter.set_delay(max(buffer_delay[0], xbar_delay[0], max(sa_delay)))


def simulate():
    while True:
        routing_algo = input("ENTER ROUTING ALGO XY/YX : ")
        if routing_algo.upper() in ["XY", "YX"]:
            routing_algo = routing_algo.upper()
            break
        else:
            print("Invalid Routing Algorithm")

    while True:
        simulation_mode = input("ENTER SIMULATION MODE PVA/PVS : ")
        if simulation_mode.upper() in ["PVA", "PVS"]:
            simulation_mode = simulation_mode.upper()
            break
        else:
            print("Invalid Simulation Mode")

    if simulation_mode == "PVA":
        buffer_delays_all = []
        sa_delays_all = []
        xbar_delays_all = []
        for _ in range(9):
            buffer_delays_all.append(buffer_delay[0])
            sa_delays_all.append(sa_delay[0])
            xbar_delays_all.append(xbar_delay[0])
        initialize(
            routing_algo,
            max(buffer_delay[0], sa_delay[0], xbar_delay[0]),
            buffer_delays_all,
            sa_delays_all,
            xbar_delays_all,
        )
        clock = Clock(
            Router_simulate_bed,
            max(buffer_delay[0], sa_delay[0], xbar_delay[0]),
            packet,
            source,
            clock_cycle,
        )
        clock.run_cycle(1000)

    elif simulation_mode == "PVS":
        mean_buffer_delay = sum(buffer_delay) / len(buffer_delay)
        mean_sa_delay = sum(sa_delay) / len(sa_delay)
        mean_xbar_delay = sum(xbar_delay) / len(xbar_delay)

        gauss_buffer_delay = generate_values(mean_buffer_delay, 1, 9)
        gauss_sa_delay = generate_values(mean_sa_delay, 2, 9)
        gauss_xbar_delay = generate_values(mean_xbar_delay, 3, 9)

        print("New Buffer Delays: ", gauss_buffer_delay)
        print("New Switch Allocator Delays: ", gauss_sa_delay)
        print("New Crossbar Delays: ", gauss_xbar_delay)

        initialize(
            routing_algo,
            max(buffer_delay[0], sa_delay[0], xbar_delay[0]),
            gauss_buffer_delay,
            gauss_sa_delay,
            gauss_xbar_delay,
        )
        clock = Clock(
            Router_simulate_bed,
            max(buffer_delay[0], sa_delay[0], xbar_delay[0]),
            packet,
            source,
            clock_cycle,
        )
        clock.run_cycle(1000)

    with open("Output/Report.txt", "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        values = line.strip().split(",")
        entry = {
            "Flit": values[0].split(": ")[1],
            "Flit Type": values[1].split(": ")[1],
            "Element": values[2].split(": ")[1],
            "Router": int(values[3].split(": ")[1]),
            "Delay": float(values[4].split(": ")[1]),
            "Clock Cycle": int(values[5].split(": ")[1]),
        }
        data.append(entry)

    grouped_data = {
        key: list(group)
        for key, group in groupby(
            sorted(data, key=itemgetter("Flit")), key=itemgetter("Flit")
        )
    }
    sorted_data = {
        key: sorted(group, key=itemgetter("Delay"))
        for key, group in grouped_data.items()
    }

    with open("Output/Report.txt", "w") as file:
        for flit, flit_data in sorted_data.items():
            file.write(f"\nFlit: {flit}\n")
            for entry in flit_data:
                file.write(
                    f"  Flit Type: {entry['Flit Type']}, Element: {entry['Element']}, Router: {entry['Router']}, Delay: {entry['Delay']}, Clock Cycle: {entry['Clock Cycle']}\n"
                )

    global_plotter.plot_latency(sorted_data)


if __name__ == "__main__":
    parser = Parser()
    buffer_delay, sa_delay, xbar_delay = parser.read_delay()
    packet, source, clock_cycle = parser.read_traffic()
    Router_simulate_bed = []

    global_logger = Logger()
    global_plotter = Plotter()
    simulate()
