class Buffer:
    def __init__(self, router):
        # Directional Buffers
        self.busy = 0
        self.North = []
        self.South = []
        self.East = []
        self.West = []

        self.my_router = router

        # PE Buffer
        self.PE_Buffer = []

        # Queue to decide where to pick
        self.pick_buffer = []

    def __repr__(self):
        return f"Buffer, Router: {self.my_router}"

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

    def read(self):
        # Check if connection Full
        if len(self.my_router.buffer_to_sa) < 1:
            flit = self.read_helper()
            if flit != None:
                self.my_router.buffer_to_sa.append(flit)
            if len(self.my_router.buffer_to_sa) > 0:
                self.my_router.logger.log(
                    self.my_router.buffer_to_sa[-1],
                    self.my_router.buffer_to_sa[-1][-2:],
                    self.my_router.clock_cycle,
                    self,
                )
                self.my_router.reporter.report(
                    self.my_router.buffer_to_sa[-1], self.my_router.clock_cycle, self
                )
        else:
            self.my_router.logger.warn(
                "SWITCH ALLOCATOR CONGESTED CANNOT STORE BUFFER DATA PACKET DELAYED"
            )

    def read_helper(self):
        read_buffer = None
        if len(self.pick_buffer) > 0:
            read_buffer = self.pick_buffer.pop(0)
        else:
            # Logging
            self.my_router.logger.warn(f"{self}: Tried reading empty buffer.")
            return None
        if read_buffer == "N" and len(self.North) > 0:
            return self.North.pop(0)
        elif read_buffer == "S" and len(self.South) > 0:
            return self.South.pop(0)
        elif read_buffer == "E" and len(self.East) > 0:
            return self.East.pop(0)
        elif read_buffer == "W" and len(self.West) > 0:
            return self.West.pop(0)
        elif read_buffer == "P" and len(self.PE_Buffer) > 0:
            return self.PE_Buffer.pop(0)
        else:
            # Logging
            self.my_router.logger.warn(f"{self}: Tried reading empty buffer.")
            return None

    def write(self, flit, write_buffer):
        if write_buffer == "N":
            self.North.append(flit)
            self.pick_buffer.append("N")
        elif write_buffer == "S":
            self.South.append(flit)
            self.pick_buffer.append("S")
        elif write_buffer == "E":
            self.East.append(flit)
            self.pick_buffer.append("E")
        elif write_buffer == "W":
            self.West.append(flit)
            self.pick_buffer.append("W")
        elif write_buffer == "P":
            self.PE_Buffer.append(flit)
            self.pick_buffer.append("P")
