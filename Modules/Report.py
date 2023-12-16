class Report:
    def __init__(self):
        self.output_file = "Output/Report.txt"
        self.file = "Config/Traffic.txt"
        open(self.output_file, "w").close()
        self.report_list = []
        self.flit_to_insertion_cycle = {}
        self.flit_type = {
            "00": "Head",
            "01": "Body",
            "10": "Tail",
        }

    def set_delay(self, delay_units=0.001):
        self.delay_units = delay_units

    def insert_flit(self, flit, cycle):
        # with self.lock:
        self.flit_to_insertion_cycle[flit] = cycle

    def report(self, flit, clock_cycle, element):
        # with self.lock:
        # if flit not in self.flit_to_insertion_cycle:
        #     return
        with open(self.file, "r") as f:
            lines = f.readlines()
            for line in lines:
                temp = line.strip().split(" ")
                if flit in [temp[2][:32],temp[2][32:64],temp[2][64:]]:
                    self.flit_to_insertion_cycle[flit] = int(temp[0])

        delay = clock_cycle - self.flit_to_insertion_cycle[flit]
        delay *= self.delay_units
        report_message = f"Flit: {flit}, Flit Type: {self.flit_type[flit[-2:]]}, Element: {element}, Delay: {delay}, Clock cycle: {clock_cycle}"
        self.report_list.append(report_message)

    def dump(self):
        with open(self.output_file, "a") as file:
            for item in self.report_list:
                file.write(str(item) + "\n")
