import os
from PIL import Image

from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs import image_tools


class ARGB2BMP(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            name = os.path.basename(self.file_name).replace('.argb', '')
            color_order = file.read(4).decode('utf-8')
            color_bit = 0

            for _ in color_order:
                color_bit += int.from_bytes(file.read(1))

            x = int.from_bytes(file.read(4), byteorder='little')
            y = int.from_bytes(file.read(4), byteorder='little')
            image_data = file.read()
            image_data = image_tools.BGR2RGB(image_data, color_order)

            image = Image.frombytes('RGBA', (x, y), image_data)
            image.save(f"{os.path.join(self.output_folder, str(name))}.{self.setting['Main']['fav_format']}")
            print(f"{localize.saving}: {name}.{self.setting['Main']['fav_format']}")

        self.update_signal.emit(100, '1/1', localize.done, True)
