class Clock:
    def __init__(self, router_bed, clock_period, packets, source, cc):
        self.Router_simulate_bed = router_bed
        self.clock_period = clock_period
        self.packets = packets
        self.source = source
        self.cc = cc

    def introduce_payload(self):
        if len(self.cc) == 0:
            return
        while self.cc[0] == self.current_cycle:
            src = self.source[0]
            i = src // 3
            j = src % 3
            payload = self.packets[0]
            self.Router_simulate_bed[i][j].buffer.write(payload, "P")
            self.Router_simulate_bed[i][j].reporter.insert_flit(payload, self.current_cycle)
            self.cc.pop(0)
            self.source.pop(0)
            self.packets.pop(0)
            if len(self.cc) == 0:
                return

    def run_cycle(self, max_cycle):
        self.current_cycle = 0
        for _ in range(max_cycle):
            self.current_cycle += 1
            self.introduce_payload()
            self.cycle()

        self.Router_simulate_bed[0][0].logger_dump()
        for row in range(3):
            for col in range(3):
                self.Router_simulate_bed[row][col].dumps()

    def cycle(self):
        for row in range(3):
            for col in range(3):
                self.Router_simulate_bed[row][col].set_clock_cycle(self.current_cycle)

        for row in range(3):
            for col in range(3):
                t = self.Router_simulate_bed[row][col].buffer.check(self.clock_period)
                if t:
                    self.Router_simulate_bed[row][col].buffer.read()
                # else:
                #     self.Router_simulate_bed[row][col].logger.warn("Delayed By 1 Clock Cycle for Router:"+str(3*row+col))

        for row in range(3):
            for col in range(3):
                t = self.Router_simulate_bed[row][col].SwitchAllocator.check(self.clock_period)
                if t:
                    self.Router_simulate_bed[row][col].SwitchAllocator.get_route()
                # else:
                #     self.Router_simulate_bed[row][col].logger.warn("Delayed By 1 Clock Cycle for Router:"+str(3*row+col))

        for row in range(3):
            for col in range(3):
                t = self.Router_simulate_bed[row][col].Xbar.check(self.clock_period)
                if t:
                    self.Router_simulate_bed[row][col].Xbar.write_to()
                # else:
                #     self.Router_simulate_bed[row][col].logger.warn("Delayed By 1 Clock Cycle for Router:"+str(3*row+col))
