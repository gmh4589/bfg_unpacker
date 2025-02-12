import os
import configparser
import numpy as np
from PIL import Image
from PyQt6.QtCore import QThread
from icecream import ic
from tkinter.filedialog import askdirectory

from source.qprocess import QProcessList
from source.reaper import Reaper, file_reaper
from source.codecs.dds_tools import DDSCreator
from source.ui import localize

setting = configparser.ConfigParser()
setting.read(os.getenv('APPDATA') + '\\bfg_unpacker\\setting.ini')


def gxt_save(name, data):
    name = f'{name}.gxt'

    with open(name, 'wb') as gxt_file:
        gxt_file.write(data)

    os.system(f'./data/ps_tools/vita/GXTConvert.exe {name}')


def dds_save(args):

    with open(args['file_name'], 'rb') as df:
        df.seek(int(args['Offset']))
        dds_data = df.read()

    dds = DDSCreator()
    cubemap = 1 if args['Cubemap'] == localize.no else 0
    out_name = os.path.basename(args['file_name']).split('.')[0]
    new_name = f"{setting['Main']['out_path']}\\{out_name}.dds"
    dds.dds_save(
        width=int(args['Width']),
        height=int(args['Height']),
        codec=args['Format'],
        mips=int(args['Mip count']),
        cubemap=cubemap,
        name=new_name,
        data=dds_data
    )


class KTXConvert(Reaper):

    @file_reaper
    def run(self) -> None:

        with open(self.file_name, 'rb') as ktx_stream:
            ktx_stream.seek(0x24)
            width = int.from_bytes(ktx_stream.read(4), byteorder="little")
            height = int.from_bytes(ktx_stream.read(4), byteorder="little")
            ktx_stream.seek(0x60)
            image_data = ktx_stream.read()

        os.makedirs(os.path.dirname(self.output_folder), exist_ok=True)
        new_image = Image.frombytes('RGBA', (width, height), image_data)
        new_image.save(self.output_folder)
        self.update_pb(1, 1, self.file_name)


def qoi_converter():
    # TODO: Write it!
    pass


def image_converter(args: dict):
    conv = ImageConverter()
    conv.out_format = args.get('Format', 'png').lower()
    conv.file_name = args.get('file_name', None)
    proc = QProcessList()
    ic(conv.file_name)

    QThread(proc.q_connect(conv, conv.file_name, header=f'{localize.convert}: {conv.file_name}...')).run()


class ImageConverter(Reaper):
    out_format = 'png'

    @file_reaper
    def run(self):
        # Full support:
        # BLP, BMP, DDS, DIB, EPS, GIF, ICNS, ICO, IM, JPEG, JP2, JPX, MSP, PCX, PFM, PNG, APNG,
        # PPM, SGI, SPI, TGA, TIFF, WEBP, XBM
        # Read only:
        # CUR, DCX, FITS, FLI, FLC, FPX, FTEX, GBR, GD, IMT, IPTC, NAA, MCIDAS, MIC, MPO, PCD,
        # PIXAR, PSD, QOI, SUN, WAL, WMF, EMF, XPM
        # Write only:
        # PALM, PDF, XV

        with open(self.file_name, "rb") as im_file:
            ext = self.file_name.split('.')[-1]
            file_name = os.path.basename(self.file_name).replace(ext, self.out_format)
            image = Image.open(im_file)

            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            if self.out_format in ("jpeg", "j", "jfif", "jpe", "jpg"):
                image = image.convert('YCbCr')
            elif self.out_format == 'pcx':
                image = image.convert('RGB')
            elif self.out_format == 'xbm':
                image = image.convert('1')

            image.save(f"{self.output_folder}\\{file_name}")

            self.update_pb(1, 1, file_name)


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

    # TODO: Localize text
    if len(codecs) != 6:
        print('В папке должно быть 6 файлов!!!')
    elif codecs.count(codecs[0]) != 6:
        print('Файлы должны иметь одинаковый формат!!!')
    elif (len(widths) != 1 and
          len(heights) != 1 and
          len(mips) != 1 and
          len(depths) != 1):
        print('Файлы должны иметь одинаковые параметры!!!')
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

