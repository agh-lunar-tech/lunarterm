from common_config import *
import struct
from utils import log
from image import image_clear, image_save, image_show, image_info

# all handlers must return a byte array object with command
# in order: 
# module id - 4 bytes
# payload - 4 bytes
# cmd id - 2 bytes

def handle_com_ping(_, serial):
    log('Sending com ping to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.COM.value, 0, CmdId.COM_C_PING.value)
    serial.write(f)

def handle_com_send_image_frame(_, serial):
    log('Sending com send_frame_image to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.COM.value, 0, CmdId.COM_C_SEND_IMAGE.value)
    serial.write(f)

def handle_cmr_set_baudrate(args_d, serial):
    log('Sending cmr set_baudrate to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.CMR.value, args_d['baudrate'].value, CmdId.CMR_C_SET_BAUD_RATE.value)
    serial.write(f)

def handle_cmr_set_mode(args_d, serial):
    log('Sending cmr set_mode to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.CMR.value, args_d['mode'].value, CmdId.CMR_C_SET_MODE.value)
    serial.write(f)

def handle_cmr_capture(args_d, serial):
    log('Sending cmr capture to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.CMR.value, args_d['memory slot'], CmdId.CMR_C_CAPTURE.value)
    serial.write(f)

def handle_cmr_download(args_d, serial):
    log('Sending cmr download to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IHHH', ModuleId.CMR.value, 
                       args_d['memory slot'],  # 2 first bytes of payload is memory slot
                       args_d['preview'], # 2 last bytes is preview
                       CmdId.CMR_C_DOWNLOAD.value)
    serial.write(f)

def handle_cmr_download_line(args_d, serial):
    log('Sending cmr download line to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IHHH', ModuleId.CMR.value, 
                       args_d['memory slot'], # same as with cmr download
                       args_d['line'], 
                       CmdId.CMR_C_DOWNLOAD_LINE.value) 
    serial.write(f)

def handle_sup_trigger_happy_path(args_d, serial):
    log('Sending sup trigger happy path to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.SUP.value, 0, CmdId.SUP_C_TRIGGER_HAPPY_PATH.value) 
    serial.write(f)

def handle_sup_run_partial(args_d, serial):
    log('Sending sup run partial to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IBBHH', ModuleId.SUP.value, 
                       args_d['start'],
                       args_d['end'],
                       0,
                       CmdId.SUP_C_RUN_PARTIAL_HAPPY_PATH.value) 
    serial.write(f)



def handle_image_clear(args_d, serial):
    log('clearing image.')
    image_clear()

def handle_image_show(args_d, serial):
    log('showing image.')
    image_show()

def handle_image_save(args_d, serial):
    log('saving image.')
    image_save('tmp.jpg')

def handle_image_info(args_d, serial):
    width, height = image_info()
    log(f'current image - width{width}, height: {height}.')


































































