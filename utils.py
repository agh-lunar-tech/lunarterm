
from enum import Enum
import argparse

def log(text):
     print('[INFO] ' + text)

class FakeQuit(Exception):
        pass

def exit(*args, **kwargs):
    raise FakeQuit

class ArgTypeMixin(Enum):
    @classmethod
    def argtype(cls, s: str) -> Enum:
        try:
            return cls[s]
        except KeyError:
            raise argparse.ArgumentTypeError(
                f"{s!r} is not a valid {cls.__name__}")

    def __str__(self):
        return self.name

def add_command_parser(module_subparsers, command_name, command_handler):
    parser = module_subparsers.add_parser(command_name)
    parser.set_defaults(func=command_handler)
    # do not exit on wrong command
    parser.exit = exit
    return parser