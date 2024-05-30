class Logger():
    def __init__(self):
        return

    @staticmethod
    def info(msg: str):
        print("INFO: ", msg)

    @staticmethod
    def warning(msg: str):
        print("WARNING: ", msg)

    @staticmethod
    def error(msg: str):
        print("ERROR: ", msg)

    @staticmethod
    def fatal(msg: str):
        print("FATAL: ", msg)
        exit(1)
