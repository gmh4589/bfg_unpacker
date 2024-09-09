import os
from icecream import ic
from collections import namedtuple
import numpy
import io
from tkinter.filedialog import askopenfilename
from PIL import Image

from source.reaper import Reaper, file_reaper
from source.ui import localize
# TODO: Add to archive creation support


class GRPExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as grp_file:
            magic = grp_file.read(4)

            if magic != b'KenS':
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Build Engine'), True)
                return

            grp_file.seek(0xC)
            file_count = int.from_bytes(grp_file.read(4), byteorder="little")
            FileList = namedtuple('FileList',
                                  ['name', 'size'])
            file_list = []

            for i in range(file_count):
                name = grp_file.read(0xC).decode("ascii").split("\0")[0]
                size = int.from_bytes(grp_file.read(4), byteorder="little")
                file_list.append(FileList(name, size))

            ic(file_list)

            for j, file in enumerate(file_list):

                with open(os.path.join(self.output_folder, file.name), 'wb') as new_file:
                    new_file.write(grp_file.read(file.size))

                self.update_pb(file_count, j + 1, file.name)


class RFFExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as rff_file:
            magic = rff_file.read(4)

            if magic != b"RFF\x1A":
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Build Engine'), True)
                return

            FileList = namedtuple('FileList',
                                  ['name', 'size', 'offset'])
            file_list = []
            file_len = os.path.getsize(self.file_name)
            version = int.from_bytes(rff_file.read(4), byteorder="little")
            file_list_start = int.from_bytes(rff_file.read(4), byteorder="little")
            file_count = int.from_bytes(rff_file.read(4), byteorder="little")
            encryption = False if version == 0x200 else True
            file_list_len = file_len - file_list_start
            rff_file.seek(file_list_start)

            if encryption:

                key = file_list_start & 0xFF
                fat = bytearray(rff_file.read(file_list_len))
                fat = numpy.array(fat, dtype=numpy.uint8)

                for i in range(file_list_len):

                    if version == 0x300:
                        fat[i] ^= (key >> 1)
                        key += 1
                    else:
                        fat[i] ^= key
                        key += (i & 1)

                files_data = io.BytesIO(fat.tobytes())
                file_list_len = len(fat)

                with open('temp.dat', 'wb') as temp:
                    temp.write(fat.tobytes())

            else:
                files_data = io.BytesIO(rff_file.read(file_list_len))

            for j in range(file_list_len):
                files_data.seek(16, 1)
                offset = int.from_bytes(files_data.read(4), byteorder="little")
                size = int.from_bytes(files_data.read(4), byteorder="little")
                files_data.seek(9, 1)
                ext = files_data.read(3).decode('ascii')
                name = files_data.read(8).decode("ascii").split("\0")[0]
                files_data.seek(4, 1)
                file_list.append(FileList(f"{name}.{ext}", size, offset))

            for k, file in enumerate(file_list):
                rff_file.seek(file.offset)
                self.update_pb(file_count - 1, k, file.name)

                if k == file_count - 1:
                    return

                with open(os.path.join(self.output_folder, file.name), 'wb') as new_file:
                    new_file.write(rff_file.read(file.size))


class ARTExtractor(Reaper):

    @file_reaper
    def run(self):
        palette_file = os.path.join(os.path.dirname(self.file_name), 'PALETTE.DAT')

        if not os.path.exists(palette_file):
            palette_file = askopenfilename(filetypes=[("Palette files", "PALETTE.DAT")])

        if not palette_file:
            self.update_signal.emit(100, '', '', True)
            return

        with open(palette_file, "rb") as palette:
            color_seq = sum([[int.from_bytes(palette.read(1)) * 4 for _ in range(3)] for i in range(256)], [])

        with open(self.file_name, "rb") as art_file:
            magic = art_file.read(4)

            if magic != b"\x01\0\0\0":
                print(localize.not_correct_file)
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Build Engine'), True)
                return

            art_file.seek(4, 1)
            start_num = int.from_bytes(art_file.read(4), byteorder="little")
            end_num = int.from_bytes(art_file.read(4), byteorder="little")
            tiles_count = end_num - start_num + 1
            heights_list = [int.from_bytes(art_file.read(2), byteorder="little") for _ in range(tiles_count)]
            widths_list = [int.from_bytes(art_file.read(2), byteorder="little") for _ in range(tiles_count)]
            art_file.seek(4 * tiles_count, 1)

            for i in range(tiles_count):
                w = widths_list[i]
                h = heights_list[i]
                size = h * w
                name = f"{str(start_num + i)}.{self.setting['Main']['fav_format']}"
                tile_data = list(art_file.read(size))

                if w != 0 and h != 0:
                    tile_data = [tile_data[i:i + w] for i in range(0, len(tile_data), w)]
                    tile_data = sum(map(list, zip(*tile_data)), [])
                    self.update_pb(tiles_count, i + 1, name)

                    with open(os.path.join(self.output_folder, name), 'wb') as new_image:
                        image = Image.new(mode="P", size=(h, w))
                        image.putpalette(color_seq)
                        image.putdata(tile_data)
                        image.save(new_image, transparency=255)

        self.update_pb(tiles_count, tiles_count, '')
