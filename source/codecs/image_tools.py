import os
import numpy as np
from PIL import Image
from PyQt6.QtCore import QThread
from icecream import ic
from tkinter.filedialog import askdirectory

from source.qprocess import QProcessList
from source.reapers.images.image_converter import ImageConverter
from source.codecs.dds_tools import DDSCreator
from source.ui import localize
from source.setting import setting

Image.MAX_IMAGE_PIXELS = 500_000_000  # 500 megapixels max image size


def gxt_save(name, data):
    name = f'{name}.gxt'

    with open(name, 'wb') as gxt_file:
        gxt_file.write(data)

    os.system(f'./data/ps_tools/vita/GXTConvert.exe {name}')


def dds_save(**kwargs):

    with open(kwargs['file_name'], 'rb') as df:
        df.seek(int(kwargs['Offset']))
        dds_data = df.read()

    dds = DDSCreator()
    cubemap = 1 if kwargs['Cubemap'] == localize.no else 0
    out_name = os.path.basename(kwargs['file_name']).split('.')[0]
    new_name = f"{setting['Main']['out_path']}\\{out_name}.dds"
    dds.dds_save(
        width=int(kwargs['Width']),
        height=int(kwargs['Height']),
        codec=kwargs['Format'],
        mips=int(kwargs['Mip count']),
        cubemap=cubemap,
        name=new_name,
        data=dds_data
    )


def image_converter(**kwargs):
    conv = ImageConverter()
    conv.out_format = kwargs.get('Format', 'png').lower()
    conv.file_name = kwargs.get('file_name', None)
    proc = QProcessList()
    ic(conv.file_name)

    QThread(proc.q_connect(conv, conv.file_name,
                           header=f'{localize.convert}: {conv.file_name}...',
                           out_dir=setting['Main']['out_path'],
                           subfolder=bool(int(setting['Main']['subfolders']))
                           )).run()


# For 24 and 32 bits
def BGR2RGB(data: bytes, color_order: str) -> bytes:
    byte_array = list(data)

    a = [byte_array[g] for g in
         range(color_order.index('A'), len(byte_array), len(color_order))] if 'A' in color_order else []
    x = [byte_array[h] for h in
         range(color_order.index('X'), len(byte_array), len(color_order))] if 'X' in color_order else []
    r = [byte_array[d] for d in range(color_order.index('R'), len(byte_array), len(color_order))]
    g = [byte_array[e] for e in range(color_order.index('G'), len(byte_array), len(color_order))]
    b = [byte_array[f] for f in range(color_order.index('B'), len(byte_array), len(color_order))]
    a = x if 'X' in color_order else a

    new_data = [item for sublist in (zip(r, g, b, a) if 'A' in color_order else zip(r, g, b)) for item in sublist]
    return bytes(new_data)


def convert_16_to_32bit(data, width, height):
    # Create an empty array for the 32-bit RGBA data
    rgba_32bit = np.zeros((height, width, 4), dtype=np.uint8)

    # Iterate over each pixel
    for i in range(height):

        for j in range(width):
            # Read 2 bytes (16 bits) for each pixel
            pixel_index = (i * width + j) * 2
            pixel_data = int.from_bytes(data[pixel_index:pixel_index + 2], byteorder='big')

            # Extract 4 bits per channel and scale to 8 bits
            r = (pixel_data >> 12) & 0x0F
            g = (pixel_data >> 8) & 0x0F
            b = (pixel_data >> 4) & 0x0F
            a = pixel_data & 0x0F

            # Scale 4-bit values to 8-bit values
            rgba_32bit[i, j] = [r * 17, g * 17, b * 17, a * 17]

    return rgba_32bit


def create_cubemap():
    path = askdirectory()

    if not path:
        return

    file_list = os.listdir(path)
    codecs = []
    widths = set()
    heights = set()
    mips = set()
    depths = set()
    head = b''
    body = b''

    for file in sorted(file_list):

        if file.split('.')[-1] == 'dds':

            with open(os.path.join(path, file), 'rb') as temp:
                temp.seek(0x54)
                codec = temp.read(4)

                if codec is not None:
                    codecs.append(codec)
                    temp.seek(9)
                    depths.add(temp.read(1))
                    temp.seek(0xC)
                    heights.add(temp.read(4))
                    widths.add(temp.read(4))
                    temp.seek(0x1C)
                    mips.add(temp.read(4))
                    start_read = 0x80 if codec != (b'\0' * 4) else 0x94

                    if not head:
                        temp.seek(0)
                        head = temp.read(start_read)

                    temp.seek(start_read)
                    body += temp.read()

    if len(codecs) != 6:
        print(localize.six_files_in_fol)
    elif codecs.count(codecs[0]) != 6:
        print(localize.one_format)
    elif (len(widths) != 1 and
          len(heights) != 1 and
          len(mips) != 1 and
          len(depths) != 1):
        print(localize.one_param)
    else:
        new_name = f"{setting['Main']['out_path']}\\out.dds"

        with open(new_name, 'wb') as new_dds:
            new_dds.write(head[:0x71] + b'\xFE' + head[0x72:] + body)


class TGACreator:

    def __init__(self, width, height, bpp, bpc, image_data):
        self.width = width
        self.height = height
        self.bpp = bpp
        self.bpc = bpc
        self.image_data = image_data

    def tga_save(self, name):

        with open(name, 'wb') as tga:
            tga.write(b'\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            tga.write(self.width.to_bytes(2, byteorder='little'))
            tga.write(self.height.to_bytes(2, byteorder='little'))
            tga.write(self.bpp.to_bytes(1, byteorder='little'))
            tga.write(self.bpc.to_bytes(1, byteorder='little'))
            tga.write(self.image_data)

