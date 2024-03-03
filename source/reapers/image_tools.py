import os
from PIL import Image

from source.reapers.codec_list import codec_list


def dds_save(y, x, codec, name, data):

    flags = codec_list[codec]['flags']
    cdc = codec_list[codec]['codec']
    bpp = codec_list[codec]['bpp']
    rgba_mask = codec_list[codec]['rgb_mask']
    h_flg = codec_list[codec]['head_flg']

    with open(f'{name}.dds', 'wb') as dds_file:
        dds_file.write(b'DDS\x20\x7C\x00\x00\x00' + h_flg +  # DDS Header
                       x.to_bytes(4, byteorder='little') +  # Height
                       y.to_bytes(4, byteorder='little') * 2 +  # width and linear size
                       b'\x01\x00\x00\x00' * 2 + b'\x00' * 44 + b'\x20\x00\x00\x00' +
                       flags + cdc + bpp + rgba_mask + b'\x08\x10\x40\x00' + b'\x00' * 16 + data)

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
