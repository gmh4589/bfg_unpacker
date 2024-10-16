import os
import configparser
from PIL import Image

from source.reaper import Reaper
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
        mips=int(args['Mip']),
        cubemap=cubemap,
        name=new_name,
        data=dds_data
    )


class KTXConvert(Reaper):

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
