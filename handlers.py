from common_config import *
import struct
from utils import log
from image import eddie_image

# all handlers must return a byte array object with command
# in order: 
# module id - 4 bytes
# payload - 4 bytes
# cmd id - 2 bytes


### supervisor handlers

def handle_sup_idle(_, serial):
    log('Sending sup idle to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.SUP.value, 0, CmdId.SUP_C_IDLE.value)
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


### sensor handlers


def handle_sen_acc_init(_, serial):
    log('Sending sen acc initialization to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.SEN.value, 0, CmdId.SEN_C_ACC_INITIALIZATION.value)
    serial.write(f)

def handle_sen_start_acc_cali(_, serial):
    log('Sending sen start acc calibration to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.SEN.value, 0, CmdId.SEN_C_START_ACC_CALIBRATION.value)
    serial.write(f)

def handle_sen_hatch_opening(args_d, serial):
    log('Sending sen hatch opening detection to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.SEN.value, args_d['detect'], CmdId.SEN_C_HATCH_OPENING_DETECTION.value)
    serial.write(f)

def handle_sen_get_all(_,serial):
    log('Sending sen get allto eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.SEN.value, 0, CmdId.SEN_C_GET_ALL.value)
    serial.write(f)

### camera handlers

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

### motor driver handlers

def handle_md_motor_enable(args_d, serial):
    log('Sending md motor enable to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, args_d['enable'], CmdId.MD_C_MOTOR_ENABLE.value)
    serial.write(f)

def handle_md_step(args_d, serial):
    log('Sending md step to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, args_d['steps'], CmdId.MD_C_STEP.value)
    serial.write(f)

def handle_md_short_phases(args_d, serial):
    log('Sending md short phases to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, 0, CmdId.MD_C_SHORT_PHASES.value)
    serial.write(f)

def handle_md_step_period(args_d, serial):
    log('Sending md step period to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, args_d['period'], CmdId.MD_C_STEP_PERIOD.value)
    serial.write(f)

def handle_md_dir(args_d, serial):
    log('Sending md dir period to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, args_d['dir'], CmdId.MD_C_DIR.value)
    serial.write(f)

def handle_md_set_mode(args_d, serial):
    log('Sending md set mode to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, args_d['mode'].value, CmdId.MD_C_SET_MODE.value)
    serial.write(f)

def handle_md_ignore_endstop(args_d, serial):
    log('Sending md ignore endstop to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.MD.value, 0, CmdId.MD_C_STEP_IGNORE_ENDSTOP.value)
    serial.write(f)

### communication handlers

def handle_com_ping(_, serial):
    log('Sending com ping to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.COM.value, 0, CmdId.COM_C_PING.value)
    serial.write(f)

def handle_com_send(_, serial):
    log('Sending com send to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.COM.value, 0, CmdId.COM_C_SEND.value)
    serial.write(f)

def handle_com_send_image_frame(_, serial):
    log('Sending com send_frame_image to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.COM.value, 0, CmdId.COM_C_SEND_IMAGE.value)
    serial.write(f)

def handle_com_send_error(_, serial):
    log('Sending com send_error to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.COM.value, 0, CmdId.COM_C_SEND_ERROR.value)
    serial.write(f)
    
### power module handlers

def handle_pm_motor_power(args_d, serial):
    log('Sending pm motor power to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.PM.value,  args_d['power'], CmdId.PM_C_MOTOR_POWER.value)
    serial.write(f)

def handle_pm_rad_power(args_d, serial):
    log('Sending pm rad power to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.PM.value,  args_d['power'], CmdId.PM_C_RAD_POWER.value)
    serial.write(f)

def handle_pm_camera_power(args_d, serial):
    log('Sending pm camera power to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.PM.value,  args_d['power'], CmdId.PM_C_CAM_POWER.value)
    serial.write(f)

def handle_pm_mram_power(args_d, serial):
    log('Sending pm mram power to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.PM.value,  args_d['power'], CmdId.PM_C_MRAM_POWER.value)
    serial.write(f)

def handle_pm_cut_thermal_knife(args_d, serial):
    log('Sending pm cut thermal knife to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.PM.value,  args_d['id'], CmdId.PM_C_CUT_THERMAL_KNIFE.value)
    serial.write(f)

def handle_pm_stop_thermal_knife(args_d, serial):
    log('Sending pm stop thermal knife to eddie.')
    f = FRAME_START_SYMBOL + struct.pack('IIH', ModuleId.PM.value,  args_d['id'], CmdId.PM_C_STOP_THERMAL_KNIFE.value)
    serial.write(f)

### internal command handlers


def handle_image_clear(args_d, serial):
    log('clearing image.')
    eddie_image.clear()

def handle_image_show(args_d, serial):
    log('showing image.')
    eddie_image.show()

def handle_image_save(args_d, serial):
    log('saving image.')
    eddie_image.save('tmp.jpg')

def handle_image_info(args_d, serial):
    width, height = eddie_image.info()
    log(f'current image - width: {width}, height: {height}.')


































































