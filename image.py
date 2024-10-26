from PIL import Image
from utils import log
import cv2
import numpy as np
import math
from pathlib import Path
from common_config import ImageType

# Mask for simplest color balance
def apply_mask(matrix, mask, fill_value):
  masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
  return masked.filled()

# Threshold for simplest color balance
def apply_threshold(matrix, low_value, high_value):
  low_mask = matrix < low_value
  matrix = apply_mask(matrix, low_mask, low_value)
  high_mask = matrix > high_value
  matrix = apply_mask(matrix, high_mask, high_value)
  return matrix

# Channel scaling
def scale_chn(img, chn, factor):
  img = img.astype('uint16')
  scale = int(2**(factor-1))
  if chn == 'r':
    b = img[:,:,0]
    g = img[:,:,1]
    r = np.clip(img[:,:,2]+scale-1, 0, 255)
  if chn == 'g':
    b = img[:,:,0]
    g = np.clip(img[:,:,1]+scale-1, 0, 255)
    r = img[:,:,2]
  if chn == 'b':
    b = np.clip(img[:,:,0]+scale-1, 0, 255)
    g = img[:,:,1]
    r = img[:,:,2]
 
  return cv2.merge((b.astype('uint8'), g.astype('uint8'), r.astype('uint8'))) 

# Simplest Color Balance Algorithm
def simplest_cb(img, percent):
  assert img.shape[2] == 3
  assert percent > 0 and percent < 100
  half_percent = percent / 200.0
  channels = cv2.split(img)
  out_channels = []
  for channel in channels:
    assert len(channel.shape) == 2
    height, width = channel.shape
    vec_size = width * height
    flat = channel.reshape(vec_size)
    assert len(flat.shape) == 1
    flat = np.sort(flat)
    n_cols = flat.shape[0]
    low_val  = flat[int(math.floor(n_cols * half_percent))]
    high_val = flat[int(math.ceil( n_cols * (1.0 - half_percent)))]
    thresholded = apply_threshold(channel, low_val, high_val)
    normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
    out_channels.append(normalized)
  return cv2.merge(out_channels)

# Contrast Limited Adaptive Histogram Equalization (CLAHE)
def apply_clahe(img):
  clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(8,8))
  lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
  l, a, b = cv2.split(lab)  # split on 3 different channels
  l2 = clahe.apply(l)  # apply CLAHE to the L-channel
  lab = cv2.merge((l2,a,b))  # merge channels
  result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
  return result

def debayer(path:Path, auto_adjust=False) ->Image:
    im = cv2.imread(path, 0) #image must be 24bit. 8bit image causes error message
    # Debayerowanie
    image = cv2.cvtColor(im, cv2.COLOR_BayerGR2RGB)
    # Adjust
    if auto_adjust:
        image = scale_chn(image, 'r', 5)
        image = scale_chn(image, 'g', 3)
        image = scale_chn(image, 'b', 1)
        image = simplest_cb(image,0.25)
        image = apply_clahe(image)

    return Image.fromarray(image)

class EddieImage():
    def __init__(self):
        self.IMAGE_HEIGHT = -1
        self.IMAGE_WIDTH = -1
        self.image_buffer = None
        self.receiving = False
        # self.cps_data = b''
        self.image_type = -1

    def clear(self):
        self.image_buffer = None
        self.receiving = False

        self.cps_data = b''

    def append_line(self, b):
        # self.image_buffer += b
        self.image_buffer.extend(b)

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
        if self.image_type == ImageType.COMP_PART or self.image_type == ImageType.COMP_FULL:
          print('saving compressed size: ', len(self.image_buffer))
          with open(filename + 'compressed', 'wb') as file:
            file.write(self.image_buffer)
          return
        
        try:
            img = Image.frombytes('L', (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), self.image_buffer)
            img.save(filename + '.bmp') 
        except Exception:
            log('not enough image data')

    def init_image_receive(self, height, width):
        self.IMAGE_HEIGHT = height
        self.IMAGE_WIDTH = width
        self.image_buffer = bytearray()
        self.receiving = True

    # def init_image_receive(self, image_type):
    #     self.image_type = image_type
    #     if image_type == ImageType.RAW_FULL:
    #        self.image_buffer = bytearray(640 * 480)
    #     elif image_type == ImageType.RAW_PART:
    #        self.image_buffer = bytearray(64 * 48)
    #     else:
    #        print('wrong image type')
    #     # self.IMAGE_HEIGHT = height
    #     # self.IMAGE_WIDTH = width
    #     # self.image_buffer = b''
    #     self.receiving = True

    def init_image_compressed(self, image_type, image_size):
        self.image_type = image_type
        if image_type == ImageType.COMP_FULL:
           self.image_buffer = bytearray(image_size)
        elif image_type == ImageType.COMP_PART:
           self.image_buffer = bytearray(image_size)
        self.receiving = True
           
    def got_entire_image(self):
        _, height = self.info()
        return height == self.IMAGE_HEIGHT 


eddie_image = EddieImage()
    

# filename = 'images/image0.bmp'
# im = cv2.imread(filename, 0) #image must be 24bit. 8bit image causes error message
# image = cv2.cvtColor(im, cv2.COLOR_BayerGR2RGB)
# cv2.imwrite('images/image1.bmp', image)
# filename = filename.split('.')
# colour_filename = filename[0] + '_colour.bmp'

# image = scale_chn(image, 'r', 5)
# image = scale_chn(image, 'g', 3)
# image = scale_chn(image, 'b', 1)
# image = simplest_cb(image,0.25)
# image = apply_clahe(image)


# cv2.imwrite('images/image0_color_adjusted.bmp', image)







