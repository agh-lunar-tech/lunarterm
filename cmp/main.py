from pathlib import Path
import logging as log
from PIL import Image
import numpy as np
import csv
import struct
import utils


if __name__=="__main__": 
    bsq = utils.read_BSQ_from_bin(Path("dec00.bin"), 4, 24, 32)
    decompressed = utils.BSQ_to_mosaic(bsq)
    Image.fromarray(decompressed).show()   



