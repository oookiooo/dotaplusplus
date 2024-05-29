class Logger():
    def __init__(self):
        return

    def info(self, msg: str):
        print("INFO: ", msg)

    def warning(self, msg: str):
        print("WARNING: ", msg)

    def error(self, msg: str):
        print("ERROR: ", msg)

    def fatal(self, msg: str):
        print("FATAL: ", msg)


logger = Logger()
