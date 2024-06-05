from enum import Enum, IntEnum
from utils import ArgTypeMixin

class CmrMode(ArgTypeMixin, Enum):
    SLEEP = 0 
    SD = 1
    HD = 2

class Baudrate(ArgTypeMixin, IntEnum):
    BR9600 = 0
    BR115200 = 1

MEMORY_SLOT_TYPE = int
MEMORY_SLOT_VALUES = [0, 1, 2, 3]

IMAGE_LINE_TYPE = int
IMAGE_LINE_VALUES = range(0, 481) #tmp

PREVIEW_TYPE = int
PREVIEW_VALUES = [0, 1]

class ModuleId(Enum):
    SEN = 0
    PM_= 1
    MD = 2
    CMR = 3
    COM = 4

class CmdId(Enum):
    IDLE = 0
    ACC_INITIALIZATION = 1
    START_ACC_CALIBRATION = 2
    HATCH_OPENING_DETECTION = 3
    SET_BAUD_RATE = 4
    SET_CMR_MODE = 5
    CAPTURE = 6
    DOWNLOAD = 7
    DOWNLOAD_LINE = 8
    MOTOR_ENABLE = 9
    STEP = 10
    SHORT_PHASES = 11
    STEP_PERIOD = 12
    DIR = 13
    SET_MODE = 14
    PING = 15
    SEND_IMAGE_FRAME = 16
    CUT_THERMAL_KNIFE = 17
    STOP_THERMAL_KNIFE = 18
    MOTOR_POWER = 19
    RAD_POWER = 20
    CAM_POWER = 21
    MRAM_POWER = 22
