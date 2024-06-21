import sys

from termcolor import colored


def log(msg: str, level: str = "INFO"):
    if level == "INFO":
        print(msg)
    elif level == "WARN":
        print(colored(msg, "yellow"))
    elif level == "ERROR":
        print(colored(msg, "red"), file=sys.stderr)
