from PIL import Image
from utils import log

class EddieImage():
    def __init__(self, id, type, is_compressed, slot, size, part_size):
        self.id = id
        self.type = type
        self.is_compressed = is_compressed
        self.slot = slot
        self.image_buffer = [0 for _ in range(size)]
        self.part_size = part_size
        self.size = size

    # data shoudl be part size len
    def add_data(self, offset, data):
        print('[INFO] adding data offset: ', offset, 'data_len:', len(data))
        current_size = self.part_size
        if offset + self.part_size > self.size:
            current_size = self.size - offset
            
        for i in range(current_size):
            self.image_buffer[offset + i] = data[i]

    def get_image(self):
        if self.type == 2:
            return Image.frombytes('L', (64, 48), bytes(self.image_buffer))
        return Image.frombytes('L', (640, 480), bytes(self.image_buffer))
    
    def show(self):
        img = self.get_image()
        img.show()

    def save(self, filename):
        img = self.get_image()
        img.save(filename) 
    

























