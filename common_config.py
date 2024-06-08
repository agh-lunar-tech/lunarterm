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
    # /* General commands */
    SUP_C_IDLE = 0

    # /* Sensors commands */
    SEN_C_ACC_INITIALIZATION = 1
    SEN_C_START_ACC_CALIBRATION = 2
    SEN_C_HATCH_OPENING_DETECTION = 3

    # /* Camera commands */
    CMR_C_SET_BAUD_RATE = 4
    CMR_C_SET_MODE = 5
    CMR_C_CAPTURE = 6
    CMR_C_DOWNLOAD = 7
    CMR_C_DOWNLOAD_LINE = 8

    # /*motor driver commands*/
    MD_C_MOTOR_ENABLE = 9
    MD_C_STEP = 10
    MD_C_SHORT_PHASES = 11
    MD_C_STEP_PERIOD = 12
    MD_C_DIR = 13
    MD_C_SET_MODE = 14

    # /* Communication commands */
    COM_C_PING = 15
    COM_C_SEND = 16
    COM_C_SEND_IMAGE = 17

    # /*power control commands*/
    PM_C_CUT_THERMAL_KNIFE = 18
    PM_C_STOP_THERMAL_KNIFE = 19
    PM_C_MOTOR_POWER = 20
    PM_C_RAD_POWER = 21
    PM_C_CAM_POWER = 22
    PM_C_MRAM_POWER = 23

    MD_C_STEP_IGNORE_ENDSTOP = 24

    SUP_C_TRIGGER_HAPPY_PATH = 25
    SUP_C_RUN_PARTIAL_HAPPY_PATH = 26