from enum import Enum
import argparse
import time as time_lib
import logging


timestamp = time_lib.strftime("%Y-%m-%d %H-%M-%S", time_lib.localtime())
logging.basicConfig(
    filename=f"logs/logs{timestamp}",      
    filemode='w',                
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)

def log(text):
    timestamp = time_lib.strftime("%Y-%m-%d %H-%M-%S", time_lib.localtime())
    logging.info(text)
    print(timestamp + '[INFO]' + text)

def log_eddie(text):
    timestamp = time_lib.strftime("%Y-%m-%d %H-%M-%S", time_lib.localtime())
    logging.info(text)
    print(timestamp + ' [EDDY] ' + text)

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