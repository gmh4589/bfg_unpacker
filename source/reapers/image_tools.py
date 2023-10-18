import os
from PIL import Image


def dds_save(x, y, codec, name, data):

    if codec == b'RGBA8':
        png_save(x, y, codec, name, BGR2RGB(data, 'ARGB'))
    elif codec == b'ARGB8':
        png_save(x, y, b'RGBA8', name, BGR2RGB(data, 'ABGR'))

    else:

        with open(f'{name}.dds', 'wb') as dds_file:
            dds_file.write(b'DDS\x20\x7C\x00\x00\x00\x07\x10\x0A\x00' +
                           x.to_bytes(4, byteorder='little') + y.to_bytes(4, byteorder='little') +
                           b'\x70\x55\x05\x00\x01\x00\x00\x00\x01' + b'\x00' * 47 +
                           b'\x20\x00\x00\x00\x04\x00\x00\x00' +
                           (codec if codec not in (b'ARGB8', b'RGBA8') else b'\x00' * 4) +
                           (b'\x00' * 4 if codec not in (b'ARGB8', b'RGBA8') else b'\x20\x00\x00\x00') +
                           (b'\x00' * 16 if codec != b'RGBA8' else b'\xFF\x00\x00\x00\x00\xFF\x00\x00'
                                                                   b'\x00\x00\xFF\x00\x00\x00\x00\xFF') +
                           b'\x00' * 19 + data)


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
