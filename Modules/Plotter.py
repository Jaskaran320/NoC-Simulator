import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self):
        self.directions = {}
        self.all_pairs = []
        self.flit_delay = {}

        self.flit_switch = {
            "00": "Head",
            "01": "Body",
            "10": "Tail",
        }

        self.links = {
            0: (0, 1),
            1: (1, 2),
            2: (3, 4),
            3: (4, 5),
            4: (6, 7),
            5: (7, 8),
            6: (0, 3),
            7: (3, 6),
            8: (1, 4),
            9: (4, 7),
            10: (2, 5),
            11: (5, 8),
            12: (0, 0),
            13: (1, 1),
            14: (2, 2),
            15: (3, 3),
            16: (4, 4),
            17: (5, 5),
            18: (6, 6),
            19: (7, 7),
            20: (8, 8),
        }

    def set_delay(self, delay_units=0.001):
        self.delay_units = delay_units

    def dump(self, direction, router_id):
        self.directions[router_id] = direction

        for dir in direction:
            if dir == "N":
                dest = router_id - 3
            elif dir == "S":
                dest = router_id + 3
            elif dir == "E":
                dest = router_id + 1
            elif dir == "W":
                dest = router_id - 1
            elif dir == "P":
                dest = router_id

            self.all_pairs.append((router_id, dest))

        if len(self.directions) == 9:
            self.plot_frequency()

    def plot_frequency(self):
        matching_keys = []
        for value in self.all_pairs:
            for key, val in self.links.items():
                if val == value:
                    matching_keys.append(key)
                    break

        matching_keys = np.array(matching_keys)
        matching_keys = np.unique(matching_keys, return_counts=True)

        plt.bar(matching_keys[0], matching_keys[1])
        plt.xticks(np.arange(21), np.arange(21))
        plt.yticks(np.arange(0, max(matching_keys[1]) + 1, 1))
        plt.title("Frequency of Flits vs Links")
        plt.xlabel("Link")
        plt.ylabel("Frequency")
        plt.savefig("Output/Frequency.png")
    
    def read_traffic(self):
        packet = []
        source = []
        clock_cycle = []
        with open("Config/Traffic.txt") as f:
            for line in f:
                temp = line.strip().split(" ")
                # print(temp)
                packet.append(temp[2][:32])
                packet.append(temp[2][32:64])
                packet.append(temp[2][64:])
                source.append(int(temp[1]))
                source.append(int(temp[1]))
                source.append(int(temp[1]))
                clock_cycle.append(int(temp[0]))
                clock_cycle.append(int(temp[0]))
                clock_cycle.append(int(temp[0]))
        return packet, source, clock_cycle

    def get_pair(self, packet):
        stack = []
        pair = []
        for flit in packet:
            if flit[-2:] == "00":
                if len(stack) > 0:
                    stack.pop(0)
                    stack.append(flit)
                else:
                    stack.append(flit)
            elif flit[-2:] == "10":
                if len(stack) > 0:
                    pair.append((stack.pop(0), flit))
                

        return pair

    def plot_latency(self, sorted_data):
        packet = []
        source = []
        clock_cycle = []
        packet,source,clock_cycle=self.read_traffic()

        pairs = self.get_pair(packet)
        latency = []

        for pair in pairs:
            for flit, flit_data in sorted_data.items():
                if flit == pair[0]:
                    start = flit_data[0]["Clock Cycle"]
                elif flit == pair[1]:
                    end = flit_data[-1]["Clock Cycle"]

            latency.append(end - start)

        plt.figure(figsize=(10, 10))
        plt.plot(np.arange(len(latency)), latency, "o-")
        plt.title("Latency of Flits vs Flit")
        plt.xlabel("Flit")
        plt.ylabel("Clock cycle")
        plt.xticks(np.arange(len(self.flit_delay)),
                    list(self.flit_delay.keys()))
        # plt.yticks(np.arange(0, max(latency) + 1, 2))
        plt.savefig("Output/Latency.png")
