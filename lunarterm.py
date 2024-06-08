import asyncio
import serial
import struct
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from time import perf_counter
from PIL import Image
from utils import FakeQuit
from cli_parser import parser
import argparse
from common_config import * 
from image import image_append_line, image_clear
from utils import log

DEFAULT_PORT = "COM24"
DEFAULT_BAUDRATE = 115200
FRAME_TIMEOUT = 0.1
DEFAULT_MODE = 0 # 0 - everything in everything out, 1 - only frames 

#states:
AWAIT_START = 0
AWAIT_TYPE = 1
AWAIT_SIZE = 2
AWAIT_PAYLOAD = 3

# (TODO add sequence of commands to send)
# macros_dict = {
#     "prep_mot" : [(MD_ID, MOTOR_ENABLE, 1), 
#                   (MD_ID, DIR, 1), 
#                   (MD_ID, STEP_PERIOD, 10), 
#                   (MD_ID, SET_MODE, 2),
#                   (PM_ID, MOTOR_POWER, 1)],
    
#     "deprep_mot" : [(MD_ID, MOTOR_ENABLE, 0),
#                     (PM_ID, MOTOR_POWER, 0)]
# }

TEXT_FRAME = b'\x00'
IMAGE_FRAME = b'\x01'

class Frame():
    def __init__(self):
        self.type = None
        self.size = 0
        self.payload = b''

    def to_string(self):
        return self.payload.decode('utf-8')

async def eddie_receive(serial):
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
                    log("TIMEOUT")
                    reset()
                await asyncio.sleep(0.001)
            out = serial.read(1)
            if state == AWAIT_START:
                if out == FRAME_START_SYMBOL:
                    state = AWAIT_TYPE
                else:
                    reset()
            elif state == AWAIT_TYPE:
                frame = Frame()
                frame.type = out
                state = AWAIT_SIZE
            elif state == AWAIT_SIZE:
                if frame.type == IMAGE_FRAME:
                    frame.size = 640
                else:
                    frame.size = int.from_bytes(out, 'little')
                state = AWAIT_PAYLOAD
            elif state == AWAIT_PAYLOAD:
                current += 1
                frame.payload += out
                # if frame.type == IMAGE_FRAME:
                #     log(f"Current {current}")
                if current == frame.size:
                    if frame.type == TEXT_FRAME:
                        print('[EDDY]', frame.to_string())
                    elif frame.type == IMAGE_FRAME:
                        print(f'[EDDY] got image frame. got {len(current_image)} bytes.')
                        image_append_line(frame.payload)
                    reset()
            start_time = perf_counter()
    except asyncio.CancelledError:
        print('asyncio.CancelledError')
    except Exception as e:
        print(e)

async def interactive_shell(serial):
    global current_image
    session = PromptSession("> ")
    while True:
        try:
            inp = await session.prompt_async()
            command_args = parser.parse_args(args=inp.split())
            if 'func' in vars(command_args):
                command_args.func(vars(command_args), serial)
        except (EOFError, KeyboardInterrupt, argparse.ArgumentError):
            return
        except FakeQuit:
            pass


async def app(port, baudrate):
    serial_port = serial.Serial(port=port, baudrate=baudrate, bytesize=8, stopbits=serial.STOPBITS_ONE)
    with patch_stdout():
        background_task = asyncio.create_task(eddie_receive(serial_port))
        try:
            await interactive_shell(serial_port)
        finally:
            background_task.cancel()
            pass

def main():
    port = input(f'Port (default: {DEFAULT_PORT}): ').strip() or DEFAULT_PORT
    baudrate = int(input(f'Baudrate (default: {DEFAULT_BAUDRATE}): ').strip() or DEFAULT_BAUDRATE)
    asyncio.run(app(port, baudrate))

if __name__ == "__main__":
    main()