import sys
from classes import*


image = Image()
image_in, image_out, scale = sys.argv[1], sys.argv[2], int(sys.argv[3])

with open(image_in, 'rb') as f:
    data = bytearray(f.read())

image.read_bmp(image_in)
image2 = image.just_zoom(scale)
image2.write_bmp(image_out)
