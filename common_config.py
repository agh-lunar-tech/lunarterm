from enum import Enum, IntEnum
from utils import ArgTypeMixin

FRAME_START_SYMBOL = b'\x12'

class CmrMode(ArgTypeMixin, Enum):
    SLEEP = 0 
    SD = 1
    HD = 2

class Baudrate(ArgTypeMixin, IntEnum):
    BR9600 = 0
    BR115200 = 1

class MDMode(ArgTypeMixin, Enum):
    FULLSTEP = 0 
    HALFSTEP_FAST = 1
    HALFSTEP_SLOW = 2


MEMORY_SLOT_TYPE = int
MEMORY_SLOT_VALUES = [0, 1, 2, 3]

IMAGE_LINE_TYPE = int
IMAGE_LINE_VALUES = range(0, 481) #tmp

PREVIEW_TYPE = int
PREVIEW_VALUES = [0, 1]

PART_TYPE = int
PART_VAL = range(0, 30)

DETECT_TYPE = int
DETECT_VALUES = [0, 1]

ENABLE_TYPE = int
ENABLE_VALUES = [0, 1]

STEPS_TYPE = int

PERIOD_TYPE = int

DIR_TYPE = int
DIR_VALUES = [0, 1]

POWER_TYPE = int

RESISTOR_ID_TYPE = int

class ModuleId(Enum):
    SEN = 0
    PM = 1
    MD = 2
    CMR = 3
    COM = 4
    SUP = 5

class CmdId(Enum):
    SUP_C_IDLE = 0

    CMR_C_SET_BAUD_RATE = 4
    CMR_C_SET_MODE = 5
    CMR_C_CAPTURE = 6
    CMR_C_DOWNLOAD = 7
    CMR_C_DOWNLOAD_LINE = 8

    COM_C_PING = 15

    COM_C_SEND = 16

    PM_C_CUT_THERMAL_KNIFE = 17
    PM_C_STOP_THERMAL_KNIFE = 18
    PM_C_RAD_POWER = 20
    PM_C_CAM_POWER = 21
    PM_C_MRAM_POWER = 22
    PM_C_TURN_ON_LED = 23
    PM_C_TURN_OFF_LED = 24

    SEN_C_ICM_INITIALIZATION = 81
    SEN_C_MMC_INITIALIZATION = 82
    SEN_C_RDN_INITIALIZATION = 83
    SEN_C_GET_ALL = 84
    SEN_C_GET_ICM = 85
    SEN_C_GET_MMC = 86
    SEN_C_GET_RDN = 87
    SEN_C_GET_ENC = 88
    SEN_C_GET_ENDSTOPS = 89

    MD_C_ENABLE = 120
    MD_C_STEPS = 121
    MD_C_ON_INF = 122
    MD_C_SET_SPEED = 123
    MD_C_SET_DIR = 124
    MD_C_STOP = 125
    MD_C_OFF = 126

    MD_C_STEP_IGNORE_ENDSTOP = 23

    SUP_C_TRIGGER_HAPPY_PATH = 24
    SUP_C_RUN_PARTIAL_HAPPY_PATH = 25

    COM_C_SEND_IMAGE = 26
    CMR_C_SET_EXPOSURE = 27