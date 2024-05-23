import asyncio
import serial
import struct
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from time import perf_counter
from PIL import Image

current_image = b''

DEFAULT_PORT = "COM24"
DEFAULT_BAUDRATE = 115200
START_SYMBOL = b'\x12'
FRAME_TIMEOUT = 0.01
DEFAULT_MODE = 0 # 0 - everything in everything out, 1 - only frames 


#module ids
SEN_ID = 0
PM_ID = 1
MD_ID = 2
CMR_ID = 3
COM_ID = 4
#etc

#command ids
IDLE = 0
ACC_INITIALIZATION = 1
START_ACC_CALIBRATION = 2
HATCH_OPENING_DETECTION = 3
SET_BAUD_RATE = 4
SET_MODE = 5
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
SEND = 16
CUT_THERMAL_KNIFE = 17
STOP_THERMAL_KNIFE = 18
MOTOR_POWER = 19
RAD_POWER = 20
CAM_POWER = 21
MRAM_POWER = 22

#states:
AWAIT_START = 0
AWAIT_TYPE = 1
AWAIT_SIZE = 2
AWAIT_PAYLOAD = 3

#command types for lunarterm use:
CMD_TO_EDDY = 0
CMD_LOCAL = 1


#macros
macros_dict = {
    "prep_mot" : [(MD_ID, MOTOR_ENABLE, 1), 
                  (MD_ID, DIR, 1), 
                  (MD_ID, STEP_PERIOD, 10), 
                  (MD_ID, SET_MODE, 2),
                  (PM_ID, MOTOR_POWER, 1)],
    
    "deprep_mot" : [(MD_ID, MOTOR_ENABLE, 0),
                    (PM_ID, MOTOR_POWER, 0)]
}

TEXT_FRAME = b'\x00'
IMAGE_FRAME = b'\x01'
# TYPE2 = b'\x02'

class Frame():
    def __init__(self):
        self.type = None
        self.size = 0
        self.payload = b''

    def to_string(self):
        return f'frame type {self.type}, with size: {self.size} and payload: {self.payload}'


async def print_frames(serial):
    global current_image

    frame = None
    state = 0
    current = 0
    start_time = 0
    def reset():
        nonlocal state, current, frame, start_time 
        state = AWAIT_START
        current = 0
        frame = None
        start_time = 0
    
    reset()
    try:
        while True:
            while serial.in_waiting == 0:
                if state != AWAIT_START and perf_counter() - start_time > FRAME_TIMEOUT:
                    print("TIMEOUT")
                    reset()
                await asyncio.sleep(0.001)
            out = serial.read(1)
            if state == AWAIT_START:
                if out == START_SYMBOL:
                    state = AWAIT_TYPE
                    start_time = perf_counter()
                else:
                    reset()
            elif state == AWAIT_TYPE:
                frame = Frame()
                frame.type = out
                state = AWAIT_SIZE
            elif state == AWAIT_SIZE:
                frame.size = int.from_bytes(out, 'little')
                state = AWAIT_PAYLOAD
            elif state == AWAIT_PAYLOAD:
                current += 1
                print(f"Current {current}")
                frame.payload += out
                if current == frame.size:
                    if frame.type == TEXT_FRAME:
                        print('[EDDY]', frame.to_string())
                    elif frame.type == IMAGE_FRAME:
                        print(f'[EDDY] got image frame. got {len(current_image)} bytes.')
                        current_image += frame.payload
                    reset()
    except asyncio.CancelledError:
        print('asyncio.CancelledError')
    except Exception as e:
        print(e)

def resolve_command(arg2):
    command = 0
    if arg2 == 'IDLE': 
        command = IDLE
    elif arg2 == 'ACC_INITIALIZATION': 
        command = ACC_INITIALIZATION
    elif arg2 == 'START_ACC_CALIBRATION': 
        command = START_ACC_CALIBRATION
    elif arg2 == 'HATCH_OPENING_DETECTION': 
        command = HATCH_OPENING_DETECTION
    elif arg2 == 'SET_BAUD_RATE': 
        command = SET_BAUD_RATE
    elif arg2 == 'SET_MODE': 
        command = SET_MODE
    elif arg2 == 'CAPTURE': 
        command = CAPTURE
    elif arg2 == 'DOWNLOAD': 
        command = DOWNLOAD
    elif arg2 == 'DOWNLOAD_LINE': 
        command = DOWNLOAD_LINE
    elif arg2 == 'MOTOR_ENABLE': 
        command = MOTOR_ENABLE
    elif arg2 == 'STEP': 
        command = STEP
    elif arg2 == 'SHORT_PHASES': 
        command = SHORT_PHASES
    elif arg2 == 'STEP_PERIOD': 
        command = STEP_PERIOD
    elif arg2 == 'DIR': 
        command = DIR
    elif arg2 == 'SET_MODE': 
        command = SET_MODE
    elif arg2 == 'PING': 
        command = PING
    elif arg2 == 'SEND': 
        command = SEND
    elif arg2 == 'CUT_THERMAL_KNIFE': 
        command = CUT_THERMAL_KNIFE
    elif arg2 == 'STOP_THERMAL_KNIFE': 
        command = STOP_THERMAL_KNIFE
    elif arg2 == 'MOTOR_POWER': 
        command = MOTOR_POWER
    elif arg2 == 'RAD_POWER': 
        command = RAD_POWER
    elif arg2 == 'CAM_POWER': 
        command = CAM_POWER
    elif arg2 == 'MRAM_POWER': 
        command = MRAM_POWER
    elif arg2 == 'PING':
        command = PING
    else:
        command = 0
    
    return command

def resolve_module(arg1):
    module = 0
    if arg1 == 'sen':
        module = SEN_ID
    elif arg1 == 'pm':
        module = PM_ID
    elif arg1 == 'md':
        module = MD_ID
    elif arg1 == 'cmr':
        module = CMR_ID
    elif arg1 == 'com':
        module = COM_ID
    else:
        module = 0

    return module

#TODO exceptions
def parse_input(inp):
    inp = inp.split()

    if len(inp) == 1:
        return (CMD_LOCAL, inp[0])

    if len(inp) != 3:
        return None
    
    arg1 = inp[0]
    arg2 = inp[1]

    if arg1 in macros_dict.keys():
        return macros_dict[arg1]

    module = 0
    command = 0
    payload = int(inp[2])

    if payload < 0:
        return None 

    # module resolve
    module = resolve_module(arg1)

    # command resolve
    command = resolve_command(arg2)

    return (CMD_TO_EDDY, [(module, command, payload)])

def build_frame(mod_id, cmd_id, payload):
    return  START_SYMBOL + struct.pack('IIH', mod_id, payload, cmd_id)

async def interactive_shell(serial):
    global current_image
    session = PromptSession("$ ")
    while True:
        try:
            inp = await session.prompt_async()
            # serial.write(inp)
            params = parse_input(inp)
            if params:
                # print('params:', params)
                if params[0] == CMD_LOCAL:
                    if params[1] == 'clear_image':
                        current_image = b''
                        print('[INFO] current image cleared')
                    elif params[1] == 'image_info':
                        print(f'[INFO] current image length: {len(current_image)}')
                    elif params[1] == 'show_image':
                        print("[INFO] image: ", current_image)
                        pass
                    else:
                        print("[INFO] Wrong command")
                else:
                    for param in params[1]:
                        if param:
                            mod_id, cmd_id, payload = param
                            frame = build_frame(mod_id, cmd_id, payload)
                            # print("[INFO] sending frame")
                            serial.write(frame)
            else:
                print("[INFO] Wrong command")
        except (EOFError, KeyboardInterrupt):
            return


async def app(port, baudrate):
    serial_port = serial.Serial(port=port, baudrate=baudrate, bytesize=8, stopbits=serial.STOPBITS_ONE)
    print_func = print_frames
    
    with patch_stdout():
        background_task = asyncio.create_task(print_func(serial_port))
        try:
            await interactive_shell(serial_port)
            # await interactive_shell(None)
        finally:
            background_task.cancel()
            pass

def main():
    # img = Image.frombytes('L', (3, 4), current_image)
    # img.show()
    port = input(f'Port (default: {DEFAULT_PORT}): ').strip() or DEFAULT_PORT
    baudrate = int(input(f'Baudrate (default: {DEFAULT_BAUDRATE}): ').strip() or DEFAULT_BAUDRATE)
    asyncio.run(app(port, baudrate))

if __name__ == "__main__":
    main()
    # serial_port = serial.Serial(port='COM10', baudrate=115200, bytesize=8, stopbits=serial.STOPBITS_ONE)
    # serial_port.write(b'x')
    # image =b''

    # while serial_port.in_waiting < 5:
    #     pass

    # out = serial_port.read(5)
    # if out == b'XOXOX':
    #     while serial_port.in_waiting == 0:
    #         pass
    #     while True:
    #         out = serial_port.read(1)
    #         image += out
    #         print('image length: ', len(image))