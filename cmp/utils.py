import cv2
import math
from PIL import Image
import numpy as np
import logging as log
from pathlib import Path
import subprocess
import os

def read_bmp_image_as_mosaic(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    # Channels
    R, G, B = cv2.split(image)
    return R


def write_Bayer_to_bin(path: Path, mosaic: np.ndarray) -> None:
    Y, X = mosaic.shape
    log.info(f'Bayer image size: Y = {Y}, X = {X}')
    cnt = 0
    with open(path, 'wb') as file:
        for y in range(0, Y):
            for x in range(0, X):
                # print(f'Index {cnt}, (x,y) ({x},{y}): {int(mosaic[y][x])}')
                byte_value = int(mosaic[y][x]).to_bytes(1, byteorder='little', signed=False)
                file.write(byte_value)
                cnt = cnt+1


def read_Bayer_from_bin(path: Path, Y: int, X: int) -> np.ndarray:
    mosaic = np.empty((Y, X), dtype=np.uint8)
    with open(path, 'rb') as file:
        for y in range(0, Y):
            for x in range(0, X):
                byte_value = int.from_bytes(file.read(1), byteorder='little', signed=False)
                mosaic[y][x] = np.uint8(byte_value)
    return mosaic


def read_BSQ_from_bin(path: Path, Z: int, Y: int, X: int) -> np.ndarray:
    bsq = np.empty((Z, Y, X), dtype=np.uint8)
    with open(path, 'rb') as file:
        for z in range(0, Z):
            for y in range(0, Y):
                for x in range(0, X):
                    byte_value = int.from_bytes(file.read(1), byteorder='little', signed=False)
                    bsq[z][y][x] = np.uint8(byte_value)
    return bsq


def write_BSQ_to_bin(path: Path, bsq: np.ndarray) -> None:
    Z, Y, X = bsq.shape
    log.info(f'BSQ image size: Z = {Z}, Y = {Y}, X = {X}')
    with open(path, 'wb') as file:
        cnt= 0
        for z in range(0, Z):
            for y in range(0, Y):
                for x in range(0, X):
                    byte_value = int(bsq[z][y][x]).to_bytes(1, byteorder='little', signed=False)
                    # print(f'Index {cnt}, (x,y,z) ({x},{y},{z}): {int(bsq[z][y][x])}')
                    file.write(byte_value)
                    cnt = cnt + 1


def mosaic_to_BSQ(mosaic: np.ndarray) -> np.ndarray:
    Y, X = mosaic.shape
    bsq = np.empty((4, int(Y/2), int(X/2)), dtype=np.uint8)
    for y in range(0, Y, 2):
        for x in range(0, X, 2):
            bsq[0][int(y/2)][int(x/2)] = mosaic[y][x] # G1
            bsq[1][int(y/2)][int(x/2)] = mosaic[y][x+1] # R
            bsq[2][int(y/2)][int(x/2)] = mosaic[y+1][x] # B
            bsq[3][int(y/2)][int(x/2)] = mosaic[y+1][x+1] # G2
    return bsq


def BSQ_to_mosaic(bsq: np.ndarray) -> np.ndarray:
    Z, Y, X = bsq.shape
    if Z != 4:
        log.warn("Input matrix is not in BSQ format")
        return None
    mosaic= np.empty((Y*2, X*2), dtype=np.uint8)
    for y in range(0, 2*Y, 2):
        for x in range(0, 2*X, 2):
            mosaic[y][x] = bsq[0][int(y/2)][int(x/2)] # G1
            mosaic[y][x+1] = bsq[1][int(y/2)][int(x/2)] # R
            mosaic[y+1][x] = bsq[2][int(y/2)][int(x/2)] # B
            mosaic[y+1][x+1] = bsq[3][int(y/2)][int(x/2)] # G2
    return mosaic

def decompress_image(file_path, output_path):
    log.info(f'Input file: {str(file_path)}')
    log.info(f'Output file: {str(output_path)}')
    command = [
        'decompressor.exe',
        '--input', str(file_path),
        '--output', str(output_path),
        '--out_format', 'BSQ',
        '--out_depth', '4'
    ]
    # Run the command
    try:
        log.info("Trying to decompress image...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        log.error(f"Error executing the command: {e}")


def parse_txt_to_bin(input:Path):
    with open(input, 'r') as file:
        contents = file.read()
    size = 0 
    # Get list of string containing rows of the image in csv format
    lists = [l for l in contents.split('\n') if l] 
    #lists = lists[0:24]
    output = input.parent / Path(f"{input.stem}.bin")
    Y = len(lists)
    X = 0
    with open(output, 'wb') as file:
        for l in lists:
            # Get vaues for each pixel in a given row
            l_formatted = [x for x in l.split(',') if x != '']
            #l_formatted = l_formatted[0:32]
            # Check for inconsistent row size
            if size > 0:
                if X != len(l_formatted):
                    log.error(f"Row size error: X={X} and row size = {len(l_formatted)}")
            X = len(l_formatted)
            # Iterate row and save values to binary
            for p in l_formatted:
                try:
                    byte_value = int(p).to_bytes(1, byteorder='little', signed=False)
                    file.write(byte_value)
                    size = size+1
                except Exception as e:
                    log.error("Error: " + str(e))
        log.info(f'Saved {size} bytes to file. Expected size is equal to {X*Y}')
    return(output, X, Y)


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