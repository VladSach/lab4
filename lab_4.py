import sys


image_in, image_out, scale = sys.argv[1], sys.argv[2], int(sys.argv[3])
with open(image_in, 'rb') as f:
    data = bytearray(f.read())
print(data)
print(image_in)
print(image_out)
print(scale)
