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
from image import eddie_image
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

class Frame():
    def __init__(self):
        self.type = None
        self.size = 0
        self.payload = b''

    def to_string(self):
        return self.payload.decode('utf-8', errors="ignore")

async def eddie_receive(serial):
    frame = None
    state = 0
    current = 0
    start_time = 0
    image_count = 0
    current_offset = 0
    def reset():
        nonlocal state, current, frame, start_time
        state = AWAIT_START
        current = 0
        frame = None
        start_time = 0
        current_offset = 0
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
                frame.size = frame_sizes[frame.type]
                state = AWAIT_PAYLOAD
            elif state == AWAIT_PAYLOAD:
                current += 1
                frame.payload += out
                if current == frame.size:
                    if frame.type == TEXT_FRAME:
                        print('[EDDY]', frame.to_string())
                    elif frame.type == CPS_IMG_FRAME:
                        log(f'binary data loading: {(100 * current_offset / len(eddie_image.image_buffer)):.2f}%')
                        for b in frame.payload:
                            eddie_image.image_buffer[current_offset] = b
                            current_offset += 1
                            print("LEN: ", len(eddie_image.image_buffer), current_offset)
                            if current_offset >= len(eddie_image.image_buffer):
                                eddie_image.save(f'images/{image_count}')
                                current_offset = 0
                                break
                    elif frame.type == ERROR_FRAME:
                        last_command, last_feedback = struct.unpack('HH', frame.payload)
                        print('[EDDY]', f'ERROR -> last command: {last_command}, last feedback: {last_feedback}') # TODO:eddie function for logging from eddie
                    elif frame.type == IMG_INIT_FRAME:
                        eddie_image.clear()
                        image_type, image_size = struct.unpack('=BI', frame.payload)
                        eddie_image.init_image_compressed(image_type, image_size)
                        print("GOT IMAGE INIT type: ", image_type, " size: ", image_size)
                    reset()
            start_time = perf_counter()
    except asyncio.CancelledError:
        print('asyncio.CancelledError')
    except Exception as e:
        print(e)

def send_command(args):
    print("sending args", args)

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
    try:
        serial_port = serial.Serial(port=port, baudrate=baudrate, bytesize=8, stopbits=serial.STOPBITS_ONE)
    except Exception:
        log('Wrong serial parameters')
        return
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
