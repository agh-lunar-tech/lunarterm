# This came up when I couldn't add dependencies beyond the stdlib for a certain script

import argparse
import sys
from common_config import *
from cli_parser import parser
from utils import FakeQuit

# class FakeQuit(Exception):
#         pass

# def add_command_parser(module_subparsers, command_name, command_handler):
#     def exit(*args, **kwargs):
#         raise FakeQuit
#     parser = module_subparsers.add_parser(command_name)
#     parser.set_defaults(func=command_handler)
#     # do not exit on wrong command
#     parser.exit = exit
#     return parser


# def custom_action(args):
#     print('GOT: ', args)


def main():
    # parser = argparse.ArgumentParser(prog='')
    # subparsers = parser.add_subparsers(help='Send command to eddie')

    # send_parser = add_command_parser(subparsers, 'send', None)
    # send_subparsers = send_parser.add_subparsers(help='Eddie modules', required=True)

    # #### communication command parser
    # com_parser = add_command_parser(send_subparsers, 'com', None)
    # com_subparsers = com_parser.add_subparsers(help='Com commands', required=True)

    # #ping command
    # add_command_parser(com_subparsers, 'ping', custom_action)
    # #send_image_command
    # add_command_parser(com_subparsers, 'send_image_frame', custom_action)


    # #### camera command parser
    # cmr_parser = add_command_parser(send_subparsers, 'cmr', None)
    # cmr_subparsers = cmr_parser.add_subparsers(help='Cmr commands', required=True)
    
    # #set_mode_command
    # bd_parser = add_command_parser(cmr_subparsers, 'set_baudrate', custom_action)
    # bd_parser.add_argument('baudrate', type=Baudrate.argtype, choices=Baudrate)
    # #set_mode_command
    # sm_parser = add_command_parser(cmr_subparsers, 'set_mode', custom_action)
    # sm_parser.add_argument('mode', type=CmrMode.argtype, choices=CmrMode)
    # #capture_command
    # c_parser = add_command_parser(cmr_subparsers, 'capture', custom_action)
    # c_parser.add_argument('memory slot', type=MEMORY_SLOT_TYPE, choices=MEMORY_SLOT_VALUES)
    # #download command
    # d_parser = add_command_parser(cmr_subparsers, 'download', custom_action)
    # d_parser.add_argument('memory slot', type=MEMORY_SLOT_TYPE, choices=MEMORY_SLOT_VALUES)
    # d_parser.add_argument('preview', type=PREVIEW_TYPE, choices=PREVIEW_VALUES) 
    # # download line command
    # dl_parser = add_command_parser(cmr_subparsers, 'download_line', custom_action)
    # dl_parser.add_argument('memory slot', type=MEMORY_SLOT_TYPE, choices=MEMORY_SLOT_VALUES)
    # dl_parser.add_argument('line', type=IMAGE_LINE_TYPE)

    #### 

    # cmr_parsers = send_subparsers.add_parser('cmr')
    # md_parsers = send_subparsers.add_parser('md')
    # pm_parsers = send_subparsers.add_parser('pm')

    # ping = com_parsers.add_parser('ping')

    # ping = com_parsers.add_subparser('send')

    # image_parser = com_subparsers.add_parser('image')

    # First, keep ArgParser from exiting on invalid input
    # readline adds capabilities to input
    try:
        import readline
    except:
        pass

    print("Enter commands. Use 'help' for info, 'exit' to leave.")
    while True:
        try:
            command = input('> ').strip()
        except KeyboardInterrupt:
            sys.stdout.write('\n')
            continue
        except EOFError:
            sys.stdout.write('\n')
            break

        if command == 'exit':
            break

        if command in ['help', 'h', '?']:
            print('MAIN USAGE MEESAAGE')
            # parser.print_help()
            continue

        try:
            command_args = parser.parse_args(args=command.split())
            print(command_args.func(vars(command_args)))
            print('LUNARTERM', 'sending command to eddir...')
        except  argparse.ArgumentError:
            print('Catching an argumentError')
        except FakeQuit:
            pass

if __name__ ==  '__main__':
    main()