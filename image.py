from PIL import Image
from utils import log

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640

image_buffer = b''

def image_clear():
    global image_buffer
    image_buffer = b''

def image_append_line(b):
    global image_buffer
    image_buffer += b

def image_info():
    global image_buffer
    return (IMAGE_WIDTH, len(image_buffer) // IMAGE_WIDTH)

def image_show():
    global image_buffer
    try:
        img = Image.frombytes('L', (IMAGE_WIDTH, IMAGE_HEIGHT), image_buffer)
        img.show()
    except ValueError:
        log('not enough image data')

def image_save(filename):
    global image_buffer
    try:
        img = Image.frombytes('L', (IMAGE_WIDTH, IMAGE_HEIGHT), image_buffer)
        img.save(filename) 
    except ValueError:
        log('not enough image data')
    

























