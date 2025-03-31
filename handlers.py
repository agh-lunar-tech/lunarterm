from common_config import *
import struct
from utils import log

### internal command handlers

def handle_image_clear(args_d, serial):
    log('clearing image.')
    # eddie_image.clear()

def handle_image_show(args_d, serial):
    log('showing image.')
    # eddie_image.show()

def handle_image_save(args_d, serial):
    log('saving image.')
    # eddie_image.save('tmp.jpg')

def handle_image_info(args_d, serial):
    width, height = eddie_image.info()
    log(f'current image - width: {width}, height: {height}.')


































































