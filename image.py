from PIL import Image
from utils import log

class EddieImage():
    def __init__(self):
        self.IMAGE_HEIGHT = 480
        self.IMAGE_WIDTH = 640
        self.image_buffer = b''

    def clear(self):
        self.image_buffer = b''

    def append_line(self, b):
        self.image_buffer += b

    def info(self):
        return (self.IMAGE_WIDTH, len(self.image_buffer) // self.IMAGE_WIDTH)

    def show(self):
        try:
            img = Image.frombytes('L', (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), self.image_buffer)
            img.show()
        except ValueError:
            log('not enough image data')

    def save(self, filename):
        try:
            img = Image.frombytes('L', (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), self.image_buffer)
            img.save(filename) 
        except ValueError:
            log('not enough image data')

eddie_image = EddieImage()
    

























