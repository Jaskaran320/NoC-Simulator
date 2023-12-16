from Modules.Router import *
from Modules.Clock import *
from Modules.Buffer import *
from Modules.Xbar import *
from Modules.SwitchAllocator import *
from Modules.Logger import *
from Modules.Report import *


class Router:
    def __init__(self, id, routing_algo, logger, plotter):
        self.buffer = Buffer(self)
        self.SwitchAllocator = SwitchAllocator(self, id, routing_algo)
        self.reporter = Report()
        self.clock_cycle = 0
        self.router_id = id
        self.logger = logger
        self.plotter = plotter
        self.buffer_to_sa = []
        self.sa_to_xbar_direction = []
        self.sa_to_xbar_flit = []
        self.logger.log(custom_log=f"Router {self} initialized.")

    def __repr__(self):
        return f"{self.router_id}"

    def create_Xbar(self):
        self.Xbar = Xbar(
            self.north_router,
            self.south_router,
            self.east_router,
            self.west_router,
            self,
        )

    def get_Buffer(self):
        return self.buffer

    def set_clock_cycle(self, clock_cycle):
        self.clock_cycle = clock_cycle

    def set_router_neighbours(self, North, South, East, West):
        self.north_router = North
        self.south_router = South
        self.east_router = East
        self.west_router = West

    def get_router_neighbours(self):
        return self.north_router, self.south_router, self.east_router, self.west_router

    def dumps(self):
        self.reporter.dump()
        self.plotter.dump(self.Xbar.direction, self.router_id)

    def logger_dump(self):
        self.logger.dump()
