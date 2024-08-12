import os
from PIL import Image


def bmp_save(x, y, b, name, image_data):

    with open(f'{name}.bmp', 'wb') as bmp_file:
        bmp_file.write(b'BM' + (len(image_data) + 0x36).to_bytes(4, byteorder='little') +
                       b'\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00' +
                       x.to_bytes(4, byteorder='little') +
                       y.to_bytes(4, byteorder='little') + b'\x01\x00' +
                       b.to_bytes(2, byteorder='little') + b'\x00\x00\x00\x00' +
                       len(image_data).to_bytes(4, byteorder='little') + (b'\x00' * 16) +
                       image_data)


def png_save(x, y, codec, name, data):
    codec = codec.decode('utf-8')[:-1]
    Image.frombytes(codec, (y, x), data).save(f'{name}.png')


def gxt_save(name, data):
    name = f'{name}.gxt'

    with open(name, 'wb') as gxt_file:
        gxt_file.write(data)

    os.system(f'./data/ps_tools/vita/GXTConvert.exe {name}')


def byte_join(r, g, b, a, color_order):
    new_data = [item for sublist in (zip(r, g, b, a) if 'A' in color_order else zip(r, g, b)) for item in sublist]
    return bytes(new_data)


# For 24 and 32 bits
def BGR2RGB(data, color_order):
    byte_array = list(data)

    a = [byte_array[g] for g in
         range(color_order.index('A'), len(byte_array), len(color_order))] if 'A' in color_order else []
    x = [byte_array[h] for h in
         range(color_order.index('X'), len(byte_array), len(color_order))] if 'X' in color_order else []
    r = [byte_array[d] for d in range(color_order.index('R'), len(byte_array), len(color_order))]
    g = [byte_array[e] for e in range(color_order.index('G'), len(byte_array), len(color_order))]
    b = [byte_array[f] for f in range(color_order.index('B'), len(byte_array), len(color_order))]

    return byte_join(r, g, b, a if 'X' not in color_order else x, color_order)
