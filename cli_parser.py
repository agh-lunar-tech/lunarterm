import argparse
import sys
from common_config import *
from handlers import *
from utils import add_command_parser, exit

parser = argparse.ArgumentParser(prog='')
parser.exit = exit
subparsers = parser.add_subparsers(help='Send command to eddie')

#### internal image command parser
com_parser = add_command_parser(subparsers, 'image', None)
com_subparsers = com_parser.add_subparsers(help='internal image commands', required=True)

#show command
add_command_parser(com_subparsers, 'show', handle_image_show)
#clear_command
add_command_parser(com_subparsers, 'clear', handle_image_clear)
#save
add_command_parser(com_subparsers, 'save', handle_image_save)
#info
add_command_parser(com_subparsers, 'info', handle_image_info)
##############################################################################


##################################################################################
#### internal image command parser
show_parser = add_command_parser(subparsers, 'cmd', None)
show_subparsers = show_parser.add_subparsers(help='trigger command for elec*nics team', required=True)


def handle_idle(_, serial):
    log('Sending sup idle to eddie new.')
    f = FRAME_START_SYMBOL + struct.pack('B', 9)
    serial.write(f)

def handle_sen_init(_, serial):
    log('Sending sen_init command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 0)
    serial.write(f)

def handle_cut_thermal(_, serial):
    log('Sending cut_thermal command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 1)
    serial.write(f)

def handle_motor_up(_, serial):
    log('Sending motor_up command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 2)
    serial.write(f)

def handle_img_capture(_, serial):
    log('Sending img_capture command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 3)
    serial.write(f)

def handle_img_download(_, serial):
    log('Sending img_download command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 4)
    serial.write(f)

def handle_img_send(_, serial):
    log('Sending img_send command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 6)
    serial.write(f)

def handle_motor_down_proc(_, serial):
    log('Sending motor_down command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 7)
    serial.write(f)
    
def handle_led_proc(_, serial):
    log('Sending led_proc command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 8)
    serial.write(f)

def handle_start_conops(_, serial):
    log('Sending start conops command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 10)
    serial.write(f)

def handle_reset_mcu(_, serial):
    log('Sending reset mcu command.')
    f = FRAME_START_SYMBOL + struct.pack('B', 100)
    serial.write(f)

def handle_thermal_tests(_, serial):
    try:
        x = int(args.x)  # Extract and convert argument to integer
        log(f'Sending thermal tests command with x = {x}.')
        f = FRAME_START_SYMBOL + struct.pack('B', 11 + x)
        serial.write(f)
    except ValueError:
        log('Invalid value for x. Please provide an integer.')

# add_command_parser(show_subparsers, 'idle', handle_idle)
# add_command_parser(show_subparsers, 'sen_init', handle_sen_init)
# add_command_parser(show_subparsers, 'cut_thermal', handle_cut_thermal)
# add_command_parser(show_subparsers, 'motor_up', handle_motor_up)
# add_command_parser(show_subparsers, 'img_capture', handle_img_capture)
# add_command_parser(show_subparsers, 'img_download', handle_img_download)
# add_command_parser(show_subparsers, 'img_send', handle_img_send)
# add_command_parser(show_subparsers, 'led_proc', handle_led_proc)
# add_command_parser(show_subparsers, 'motor_down', handle_motor_down_proc)
# add_command_parser(show_subparsers, 'start_conops', handle_start_conops)
add_command_parser(show_subparsers, 'reset', handle_reset_mcu)

# thermal_test_parser = add_command_parser(show_subparsers, 'run_thermal_test', handle_thermal_tests)
# thermal_test_parser.add_argument('x', type=int, help='Number to add to base command 11')



