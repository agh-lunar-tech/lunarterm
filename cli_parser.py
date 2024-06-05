import argparse
import sys
from common_config import *
from handlers import *
from utils import add_command_parser, exit

parser = argparse.ArgumentParser(prog='')
parser.exit = exit
subparsers = parser.add_subparsers(help='Send command to eddie')

send_parser = add_command_parser(subparsers, 'send', None)
send_subparsers = send_parser.add_subparsers(help='Eddie modules', required=True)

#### communication command parser
com_parser = add_command_parser(send_subparsers, 'com', None)
com_subparsers = com_parser.add_subparsers(help='Com commands', required=True)

#ping command
add_command_parser(com_subparsers, 'ping', handle_com_ping)
#send_image_command
add_command_parser(com_subparsers, 'send_image_frame', handle_com_send_image_frame)


#### camera command parser
cmr_parser = add_command_parser(send_subparsers, 'cmr', None)
cmr_subparsers = cmr_parser.add_subparsers(help='Cmr commands', required=True)

#set_baudrate_command
bd_parser = add_command_parser(cmr_subparsers, 'set_baudrate', handle_cmr_set_baudrate)
bd_parser.add_argument('baudrate', type=Baudrate.argtype, choices=Baudrate)
#set_mode_command
sm_parser = add_command_parser(cmr_subparsers, 'set_mode', handle_cmr_set_mode)
sm_parser.add_argument('mode', type=CmrMode.argtype, choices=CmrMode)
#capture_command
c_parser = add_command_parser(cmr_subparsers, 'capture', handle_cmr_capture)
c_parser.add_argument('memory slot', type=MEMORY_SLOT_TYPE, choices=MEMORY_SLOT_VALUES)
#download command
d_parser = add_command_parser(cmr_subparsers, 'download', handle_cmr_download)
d_parser.add_argument('memory slot', type=MEMORY_SLOT_TYPE, choices=MEMORY_SLOT_VALUES)
d_parser.add_argument('preview', type=PREVIEW_TYPE, choices=PREVIEW_VALUES) 
# download line command
dl_parser = add_command_parser(cmr_subparsers, 'download_line', handle_cmr_download_line)
dl_parser.add_argument('memory slot', type=MEMORY_SLOT_TYPE, choices=MEMORY_SLOT_VALUES)
dl_parser.add_argument('line', type=IMAGE_LINE_TYPE)