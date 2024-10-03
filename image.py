from PIL import Image
from utils import log

class EddieImage():
    def __init__(self):
        self.IMAGE_HEIGHT = -1
        self.IMAGE_WIDTH = -1
        self.image_buffer = b''
        self.receiving = False

    def clear(self):
        self.image_buffer = b''
        self.receiving = False

    def append_line(self, b):
        self.image_buffer += b

    def info(self):
        return (self.IMAGE_WIDTH, len(self.image_buffer) // self.IMAGE_WIDTH)
    
    def info_percent(self):
        return self.info()[1] / self.IMAGE_HEIGHT * 100 

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

    def init_image_receive(self, height, width):
        self.IMAGE_HEIGHT = height
        self.IMAGE_WIDTH = width
        self.image_buffer = b''
        self.receiving = True

    def got_entire_image(self):
        _, height = self.info()
        return height == self.IMAGE_HEIGHT 


eddie_image = EddieImage()
    

























