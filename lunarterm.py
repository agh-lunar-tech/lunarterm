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
from frames_proto import lunaris_downlink_pb2
import json,csv
import os
import time as time_lib

DEFAULT_PORT = "/dev/ttyUSB1"
DEFAULT_BAUDRATE = 115200
FRAME_TIMEOUT = 0.4
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

    def telemetry_pretty_print(self):
        pass
        # f =  b'\x00\x00\x00\x06' + self.payload
        # print(f)
        # sensor_data = lunaris_downlink_pb2.SensorData()
        # try:
        #     sensor_data.ParseFromString(f)
        #     print(sensor_data)

        # except Exception as e:
        #     print("Error during deserialization:", e)
        
    def telemetry_parse_data(self):

        format_str = "<3h 3h h 3i h 6I 2h 2? 3B H"
        field_names = [
            "icm_gyr_data.x", "icm_gyr_data.y", "icm_gyr_data.z",
            "icm_acc_data.x", "icm_acc_data.y", "icm_acc_data.z",
            "icm_temp", "mmc_mag_data.x", "mmc_mag_data.y", "mmc_mag_data.z",
            "mmc_temp", "rdn_serial_dose", "rdn_sen1_dose", "rdn_sen2_dose",
            "rdn_serial_intensity", "rdn_sen1_intensity", "rdn_sen2_intensity",
            "rdn_temp", "rdn_vdd", "rdn_crystal_ok", "rdn_analog_ok",
            "encoder_sensor", "hall_endstop", "reflective_endstop", "light_sensor"
        ]
        
        unpacked_data = struct.unpack(format_str, self.payload)
        sensor_data = dict(zip(field_names, unpacked_data))
    
        return sensor_data

    def telemetry_ugly_print(self):
        sensor_data = self.telemetry_parse_data()
        for key, value in sensor_data.items():
            print(f"{key}: {value}")


    def telemetry_dump_json( self,output_path="log/last_telemetry.json"):
        sensor_data = self.telemetry_parse_data()
        json_data = json.dumps(sensor_data, indent=4)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(json_data)
        
        return json_data

    def telemetry_dump_csv(self, timestamp, output_csv="log/telemetry_data.csv" ):
        sensor_data = self.telemetry_parse_data()
        sensor_data_with_time = {"time": timestamp, **sensor_data}        
        file_exists = os.path.exists(output_csv)
        
        with open(output_csv, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["time"] + list(sensor_data.keys()))
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(sensor_data_with_time)
                
    def log(self):
        pass


async def eddie_receive(serial):
    frame = None
    state = 0
    current = 0
    start_time = 0
    image_count = 0
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
                frame.size = frame_sizes[frame.type]
                if frame.type == IMAGE_FRAME and not eddie_image.receiving:
                    eddie_image.init_image_receive(480, 640)
                elif frame.type == IMAGE_PREV_FRAME and not eddie_image.receiving:
                    eddie_image.init_image_receive(48, 64)
                state = AWAIT_PAYLOAD
            elif state == AWAIT_PAYLOAD:
                current += 1
                frame.payload += out
                if current == frame.size:
                    if frame.type == TEXT_FRAME:
                        print('[EDDY]', frame.to_string())
                    elif frame.type == IMAGE_FRAME or frame.type == IMAGE_PREV_FRAME:
                        eddie_image.append_line(frame.payload)
                        log(f'image loading: {eddie_image.info_percent():.2f}%')
                        if eddie_image.got_entire_image():
                            log('got image from eddie')
                            eddie_image.save(f'images/image{image_count}.jpg')
                            image_count += 1
                            eddie_image.show()
                            eddie_image.clear()
                    elif frame.type == TELEMETRY_FRAME:
                        print('[INFO] - Telemetry frame received')
                        frame.telemetry_ugly_print()

                        timestamp = time_lib.strftime("%Y-%m-%d %H:%M:%S", time_lib.gmtime())
                        frame.telemetry_dump_json()
                        frame.telemetry_dump_csv(timestamp)

                    elif frame.type == ERROR_FRAME:
                        last_command, last_feedback = struct.unpack('HH', frame.payload)
                        print('[EDDY]', f'ERROR -> last command: {last_command}, last feedback: {last_feedback}') # TODO:eddie function for logging from eddie
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
