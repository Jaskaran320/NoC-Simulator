class SwitchAllocator:
    def __init__(self, router, id, mode):
        self.curr_packet = None
        self.busy = 0
        self.my_router = router
        self.row = id // 3
        self.col = id % 3
        self.mode = mode
        self.routing_dictionary = (
            self.get_routing_dictionary_xy(self.row, self.col)
            if self.mode == "XY"
            else self.get_routing_dictionary_yx(self.row, self.col)
        )
        self.destination_router = None

    def __repr__(self):
        return f"Switch Allocator, Router: {self.my_router}"

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

    def get_routing_dictionary_xy(self, src_row, src_col):
        routing_dict = {}
        for i in range(3):
            for j in range(3):
                if i == src_row and j == src_col:
                    routing_dict[3 * i + j] = "P"
                elif j > src_col:
                    routing_dict[3 * i + j] = "E"
                elif j < src_col:
                    routing_dict[3 * i + j] = "W"
                elif i > src_row:
                    routing_dict[3 * i + j] = "S"
                elif i < src_row:
                    routing_dict[3 * i + j] = "N"
        return routing_dict

    def get_routing_dictionary_yx(self, src_row, src_col):
        routing_dict = {}
        for i in range(3):
            for j in range(3):
                if i == src_row and j == src_col:
                    routing_dict[3 * i + j] = "P"
                elif i > src_row:
                    routing_dict[3 * i + j] = "S"
                elif i < src_row:
                    routing_dict[3 * i + j] = "N"
                elif j > src_col:
                    routing_dict[3 * i + j] = "E"
                elif j < src_col:
                    routing_dict[3 * i + j] = "W"
        return routing_dict

    def set_dest(self, flit, dest):
        if len(self.my_router.sa_to_xbar_direction) < 10:
            self.my_router.sa_to_xbar_direction.append(dest)
            self.my_router.sa_to_xbar_flit.append(flit)
        else:
            self.my_router.logger.warn(
                f"{self}: Xbar Congested, Packet - " + flit + "Dropped/Delayed."
            )

    def get_routing_dictionary(self):
        return self.routing_dictionary

    def set_mode(self, mode):
        self.mode = mode

    def get_route(self):
        flit = self.curr_packet
        self.curr_packet = None
        if len(self.my_router.buffer_to_sa) > 0:
            self.curr_packet = self.my_router.buffer_to_sa[0]
            self.my_router.buffer_to_sa.pop(0)

        # Logging
        if flit != None:
            self.my_router.logger.log(flit, flit[-2:], self.my_router.clock_cycle, self)
            self.my_router.reporter.report(flit, self.my_router.clock_cycle, self)

        if flit == None:
            # Logging
            self.my_router.logger.warn(f"{self}: Buffer empty, nothing to allocate.")
            # print("ERROR: Invalid flit length/No Flit")
            return None

        type = flit[30:]
        if type == "00":
            binary_destination = flit[:15]
            self.destination_router = int(binary_destination, 2)
            self.set_dest(flit, self.routing_dictionary[self.destination_router])
            return self.routing_dictionary[self.destination_router]
        
        elif self.destination_router == None:
            self.my_router.logger.warn(f"{self}: Destination router not set. ")

        elif type == "01":
            self.set_dest(flit, self.routing_dictionary[self.destination_router])
            return self.routing_dictionary[self.destination_router]

        elif type == "10":
            temp = self.destination_router
            self.destination_router = None
            self.set_dest(flit, self.routing_dictionary[temp])
            return self.routing_dictionary[temp]

        else:
            print("ERROR: Invalid flit type")
            # Logging
            self.my_router.logger.warn(f"{self}: Invalid flit recieved ({flit}).")
            return None
