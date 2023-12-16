from Modules.Router import *


class Parser:
    def __init__(self):
        print("Parser initialized for reading traffic and delays file")
        pass

    def read_delay(self):
        sa_delay = []
        xbar_delay = []
        buffer_delay = []

        with open("Config/Delay.txt") as f:
            lines = f.readlines()
            for line in lines:
                temp = line.split(" ")
                sa_delay.append(float(temp[1]))
                xbar_delay.append(float(temp[2]))
                buffer_delay.append(float(temp[0]))

        return buffer_delay, sa_delay, xbar_delay

    def read_traffic(self):
        packet = []
        source = []
        clock_cycle = []
        with open("Config/Traffic.txt") as f:
            for line in f:
                temp = line.strip().split(" ")
                # print(temp)
                # print(len(temp[2][:32]),len(temp[2][32:64]))
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
