from common_config import *
import struct

# all handlers must return a byte array object with command
# in order: 
# module id - 4 bytes
# payload - 4 bytes
# cmd id - 2 bytes


# tutaj robiona jest logika caly send itp

def handle_com_ping(args):
    return struct.pack('IIH', ModuleId.COM.value, 0, CmdId.PING.value)

def handle_com_send_image_frame(args):
    return struct.pack('IIH', ModuleId.COM.value, 0, CmdId.SEND_IMAGE_FRAME.value)

def handle_cmr_set_baudrate(args_d):
    return struct.pack('IIH', ModuleId.CMR.value, args_d['baudrate'].value, CmdId.SET_BAUD_RATE.value)

def handle_cmr_set_mode(args_d):
    return struct.pack('IIH', ModuleId.CMR.value, args_d['mode'].value, CmdId.SET_CMR_MODE.value)

def handle_cmr_capture(args_d):
    return struct.pack('IIH', ModuleId.CMR.value, args_d['memory slot'], CmdId.CAPTURE.value)

def handle_cmr_download(args_d):
    return struct.pack('IHHH', ModuleId.CMR.value, 
                       args_d['memory slot'],  # 2 first bytes of payload is memory slot
                       args_d['preview'], # 2 last bytes is preview
                       CmdId.DOWNLOAD.value)

def handle_cmr_download_line(args_d):
    return struct.pack('IHHH', ModuleId.CMR.value, 
                       args_d['memory slot'], # same as with cmr download
                       args_d['line'], 
                       CmdId.DOWNLOAD_LINE.value) 

































































