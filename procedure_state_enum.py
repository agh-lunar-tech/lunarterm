from enum import Enum

class ProcedureState( Enum ):
    SEN_INIT_PROC = 0
    THERMAL_KNIFE_PROC = 1
    MOTOR_UP_PROC = 2
    IMAGE_CAPTURE_PROC = 3
    IMAGE_DOWNLOAD_PROC = 4
    COMPRESSION_PROC = 5
    MOTOR_DOWN_PROC = 6
    LED_PROC = 7
    IDLE_PROC = 8