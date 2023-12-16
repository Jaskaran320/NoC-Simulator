from Modules.Router import *
from Modules.Clock import *
from Modules.Buffer import *
from Modules.SwitchAllocator import *
from Modules.Logger import *


class Xbar:
    def __init__(self, North_router, South_router, East_router, West_router, router):
        self.busy = 0
        self.curr_direction = None
        self.curr_flit = None
        self.north_buffer = North_router.buffer if North_router != None else None
        self.south_buffer = South_router.buffer if South_router != None else None
        self.east_buffer = East_router.buffer if East_router != None else None
        self.west_buffer = West_router.buffer if West_router != None else None
        self.my_router = router
        self.direction = []

    def __repr__(self):
        return f"Xbar, Router: {self.my_router}"

    def set_delay(self, delay=0.001):
        self.delay = delay
        self.delay_check = delay

    def check(self, clock_period):
        self.delay_check -= clock_period
        if self.delay_check <= 0:
            self.delay_check = self.delay
            return True
        else:
            return False

    def packet_recieved(self, flit):
        print(flit, "at", self.my_router.router_id)

        # Logging
        # self.my_router.logger.log(
        #     custom_log=f"Flit {flit} recieved at processing element in Router {self.my_router} at Cycle {self.my_router.clock_cycle-1}"
        # )
        # self.my_router.reporter.report(flit, self.my_router.clock_cycle - 1, self)

    def write_to(self):
        direction = self.curr_direction
        flit = self.curr_flit
        # set to Null after recieving
        self.curr_direction = None
        self.curr_flit = None
        # Assign new for Next Cycle
        if len(self.my_router.sa_to_xbar_direction) > 0:
            self.curr_direction = self.my_router.sa_to_xbar_direction[0]
            self.curr_flit = self.my_router.sa_to_xbar_flit[0]
            self.my_router.sa_to_xbar_direction.pop(0)
            self.my_router.sa_to_xbar_flit.pop(0)
        # flit = self.my_buffer.Read()
        if direction == "N":
            # self.north_buffer.busy = 1
            self.north_buffer.write(flit, "S")
            self.direction.append("N")
        elif direction == "S":
            # self.south_buffer.busy = 1
            self.south_buffer.write(flit, "N")
            self.direction.append("S")
        elif direction == "E":
            # self.east_buffer.busy = 1
            self.east_buffer.write(flit, "W")
            self.direction.append("E")
        elif direction == "W":
            # self.west_buffer.busy = 1
            self.west_buffer.write(flit, "E")
            self.direction.append("W")
        elif direction == "P":
            # print("Receiving Packet")
            # self.my_router.buffer.write(flit, "P")
            self.packet_recieved(flit)
            self.direction.append("P")

        # Logging
        if flit != None:
            self.my_router.logger.log(flit, flit[-2:], self.my_router.clock_cycle, self)
            self.my_router.reporter.report(flit, self.my_router.clock_cycle, self)
