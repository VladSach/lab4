import sys
from classes import*


image = Image()
with open(image_in, 'rb') as f:
    data = bytearray(f.read())
image_in, image_out, scale = sys.argv[1], sys.argv[2], int(sys.argv[3])

image.read(image_in)
image2 = image.scale(scale)
image2.write(image_out)
