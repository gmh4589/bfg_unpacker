import os

import numpy
from PIL import Image

from source.codecs.image_tools import bmp_save
from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs import image_tools


class ARGB2BMP(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            name = os.path.join(self.output_folder, os.path.basename(self.file_name).replace('.argb', ''))
            color_order = file.read(4).decode('utf-8')
            color_bit = 0

            for _ in color_order:
                color_bit += int.from_bytes(file.read(1))

            x = int.from_bytes(file.read(4), byteorder='little')
            y = int.from_bytes(file.read(4), byteorder='little')
            image_data = file.read()
            image_data = image_tools.BGR2RGB(image_data, color_order)

            Image.frombytes('RGBA', (x, y), image_data).save(name + '.png')
            Image.frombytes('RGBA', (x, y), image_data).save(name + '.bmp')
            print(f'{localize.saving}: {name}.png')
            print(f'{localize.saving}: {name}.bmp')

        self.update_signal.emit(100, '1/1', localize.done, True)


class ArenaTexture(Reaper):

    @file_reaper
    def run(self):
        name = os.path.basename(self.file_name).replace('.', '_')
        # TODO: Find image sizes

        with open(self.file_name, 'rb') as tex:
            tex.seek(218)
            tex_data = tex.read()
            x = int(numpy.sqrt(len(tex_data))/2)

        Image.frombytes('RGBA', (x, x), tex_data).save(name + '.png')
        Image.frombytes('RGBA', (x, x), tex_data).save(name + '.bmp')
        self.update_signal.emit(100, '1/1', localize.done, True)
