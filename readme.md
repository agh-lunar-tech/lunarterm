# lunarterm.py

## Setup

- (optional) Setup a virtual environment by running `python -m venv .venv`
- Install required packages with `pip install -r requirements.txt`

## Usage:

\<module> \<command> \<payload>

example usage:
sen x y - send command with id x, and payload y to sensor module.

macros list:

- prep_mot - enables motor, sets dir to 1, sets interval to 10 ms, sets mode to 2, turns on power
- deprep_mot - disables motor, turns off power

module list:

- sen - sensors
- pm - power manager
- md - motor driver
- cmr - camera
- com - communication

command list:

- IDLE
- ACC_INITIALIZATION
- START_ACC_CALIBRATION
- HATCH_OPENING_DETECTION
- SET_BAUD_RATE
- SET_MODE
- CAPTURE
- DOWNLOAD
- DOWNLOAD_LINE
- MOTOR_ENABLE
- STEP
- SHORT_PHASES
- STEP_PERIOD
- DIR
- SET_MODE
- PING
- SEND
- CUT_THERMAL_KNIFE
- STOP_THERMAL_KNIFE
- MOTOR_POWER
- RAD_POWER
- CAM_POWER
- MRAM_POWER
