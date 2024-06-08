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

#### supervisor command parser
sup_parser = add_command_parser(send_subparsers, 'sup', None)
sup_subparsers = sup_parser.add_subparsers(help='Supervisor commands', required=True)


#idle command
add_command_parser(sup_subparsers, 'idle', handle_sup_idle)
#trigger happy path
add_command_parser(sup_subparsers, 'trigger', handle_sup_trigger_happy_path)
#run happy path part
p_parser = add_command_parser(sup_subparsers, 'part', handle_sup_run_partial)
p_parser.add_argument('start', type=PART_TYPE)
p_parser.add_argument('end', type=PART_TYPE)
##############################################################################

#### sensors command parser
sen_parser = add_command_parser(send_subparsers, 'sen', None)
sen_subparsers = sen_parser.add_subparsers(help='Sensor commands', required=True)


#acc init command
add_command_parser(sen_subparsers, 'acc_init', handle_sen_acc_init)
#start acc calibration command
add_command_parser(sen_subparsers, 'acc_cali', handle_sen_start_acc_cali)
#hatch open detection command
p_parser = add_command_parser(sen_subparsers, 'hatch_open_detect', handle_sen_hatch_opening)
p_parser.add_argument('detect', type=DETECT_TYPE, choices=DETECT_VALUES)
##############################################################################

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
##############################################################################


#### md command parser
md_parser = add_command_parser(send_subparsers, 'md', None)
md_subparsers = md_parser.add_subparsers(help='Motor driver commands', required=True)

#enable command
en_parser = add_command_parser(md_subparsers, 'enable', handle_md_motor_enable)
en_parser.add_argument('enable', type=ENABLE_TYPE, choices=ENABLE_VALUES)
#set_mode_command
step_parser = add_command_parser(md_subparsers, 'step', handle_md_step)
step_parser.add_argument('steps', type=STEPS_TYPE)
#short phases command
short_p_parser = add_command_parser(md_subparsers, 'short_phases', handle_md_short_phases)
#step period command
step_p_parser = add_command_parser(md_subparsers, 'step_period', handle_md_step_period)
step_p_parser.add_argument('period', type=PERIOD_TYPE)
# dir command
dir_parser = add_command_parser(md_subparsers, 'dir', handle_md_dir)
dir_parser.add_argument('dir', type=DIR_TYPE, choices=DIR_VALUES)
# set mode command
md_sm_parser = add_command_parser(md_subparsers, 'set_mode', handle_md_set_mode)
md_sm_parser.add_argument('mode', type=MDMode.argtype, choices=MDMode)
# md step ignore endstop command
md_ignore = add_command_parser(md_subparsers, 'ignore_endstop', handle_md_ignore_endstop)
##############################################################################



#### communication command parser
com_parser = add_command_parser(send_subparsers, 'com', None)
com_subparsers = com_parser.add_subparsers(help='Com commands', required=True)

#ping command
add_command_parser(com_subparsers, 'ping', handle_com_ping)
#send command
add_command_parser(com_subparsers, 'send', handle_com_send)
#send_image_command
add_command_parser(com_subparsers, 'send_image_frame', handle_com_send_image_frame)
##############################################################################



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