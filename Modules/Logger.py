class Logger:
    def __init__(self):
        self.output_file = "Output/Log.txt"
        open(self.output_file, "w").close()
        self.log_list = []
        self.flit_switch = {
            "00": "Head",
            "01": "Body",
            "10": "Tail",
        }

    def warn(self, msg):
        log_message = f"[WARN]: {msg}"
        self.log_list.append(log_message)

    def log(self, msg=None, flit_type=None, cycle=None, router_element=None, custom_log=None):
        if not custom_log:
            log_message = f"[FLIT]: {msg}, Flit Type: {self.flit_switch[flit_type]}, Cycle: {cycle}, Router Element: {router_element}"
        else:
            log_message = f"[DBUG]: {custom_log}"

        self.log_list.append(log_message)

    # def write_to_log(self, message):
    #     self.log_list.append(message)
    # with open(self.output_file, "a") as f:
    #     f.write(message + "\n")

    def dump(self):
        with open(self.output_file, "a") as file:
            for item in self.log_list:
                file.write(str(item) + "\n")
