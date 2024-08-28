import os
import numpy
from PIL import Image
from tkinter.filedialog import askopenfilename

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

            image = Image.frombytes('RGBA', (x, y), image_data)
            image.save(f"{name}.{self.setting['Main']['fav_format']}")
            print(f"{localize.saving}: {name}.{self.setting['Main']['fav_format']}")

        self.update_signal.emit(100, '1/1', localize.done, True)


class ArenaTexture(Reaper):

    @file_reaper
    def run(self):
        name = os.path.basename(self.file_name).replace('.', '_')
        path = os.path.join(self.output_folder, name)
        palette = askopenfilename(filetypes=[("Palette files", "*.pal, *.col")])
        # TODO: Find image sizes

        with open(palette, 'rb') as pal:
            pal.seek(8)
            color_seq = sum([[int.from_bytes(pal.read(1)) for _ in range(3)] for _ in range(256)], [])

        with open(self.file_name, 'rb') as tex:
            tex.seek(0x100)
            tex_data = tex.read()
            x = int(numpy.sqrt(len(tex_data)))

        image = Image.frombytes('P', (256, 256), tex_data)
        image.putpalette(color_seq)
        image.save(f"{path}.{self.setting['Main']['fav_format']}")
        print(f"{localize.saving}: {name}.{self.setting['Main']['fav_format']}")
        self.update_signal.emit(100, '1/1', localize.done, True)
