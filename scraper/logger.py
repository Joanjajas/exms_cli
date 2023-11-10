import sys


def log(msg: str, level: str = "INFO"):
    if level == "INFO":
        print(msg)
    elif level == "ERROR":
        print(msg, file=sys.stderr)
