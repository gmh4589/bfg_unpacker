import os

from PIL import Image
from source.reaper import Reaper, file_reaper


class WastelandPortraits(Reaper):
    # For portraits.bin only

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as ws_bin:
            dim = [(96, 84), (288, 252)]
            size = os.path.getsize(self.file_name)
            here = ws_bin.tell()
            dim_size = False
            file_num = 0

            while True:
                width, height = dim[dim_size]
                data = ws_bin.read(width * height * 3)

                try:
                    image = Image.frombytes('RGB', (width, height), data)
                    path = f"{self.output_folder}\\{str(file_num).rjust(4, '0')}.png"
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    image.save(path)
                    dim_size = not dim_size
                    here = ws_bin.tell()
                    file_num += 1
                    self.update_pb(size, here, path)

                except ValueError:
                    break

            self.update_pb(size, size, path)


class WastelandParagraphs(Reaper):
    # For paragraphs.bin and legals.bin only

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as ws_bin:
            size = os.path.getsize(self.file_name)
            here = ws_bin.tell()
            file_num = 0

            while True:
                here = ws_bin.tell()

                if file_num > 170:
                    print('Hello!')

                while True:
                    temp = int.from_bytes(ws_bin.read(1))

                    if temp > 0:
                        ws_bin.seek(here)
                        break
                    else:
                        here = ws_bin.tell()

                try:
                    width = int.from_bytes(ws_bin.read(4), 'little')
                    height = int.from_bytes(ws_bin.read(4), 'little')
                    data = ws_bin.read(width * height)
                    image = Image.frombytes('L', (width, height), data)
                    path = f"{self.output_folder}\\{str(file_num).rjust(4, '0')}.png"
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    image.save(path)
                    file_num += 1
                    self.update_pb(size, here, path)

                except (ValueError, OverflowError):
                    break

            self.update_pb(size, size, path)

class WastelandSplash(Reaper):
    # For splash.bin only

    @file_reaper
    def run(self, width=1280, height=720, count=2):

        with open(self.file_name, 'rb') as ws_bin:

            for i in range(count):
                data = ws_bin.read(width * height * 3)
                image = Image.frombytes('RGB', (width, height), data)
                path = f"{self.output_folder}\\splash_{i}.png"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                image.save(path)
                self.update_pb(count, i, path)
