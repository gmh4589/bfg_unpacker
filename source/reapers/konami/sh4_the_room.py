
from source.reaper import Reaper, file_reaper
import os
from pprint import pprint


class BINExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bin_file:
            # magic = bin_file.read(4)
            #
            # if not self.magic([b'\x10\xFA\x00\x00'], magic, 'Silent Hill 4: The Room'):
            #     return

            file_size = os.path.getsize(self.file_name)
            file_count = int.from_bytes(bin_file.read(4), byteorder="little")
            offsets = []

            for _ in range(file_count):
                offsets.append(int.from_bytes(bin_file.read(4), byteorder="little"))

            offsets.append(file_size)

            for i in range(file_count):
                bin_file.seek(offsets[i])
                data = bin_file.read(offsets[i + 1] - offsets[i])
                path = f"{self.output_folder}\\{os.path.basename(self.file_name)}_{i}.dat"
                self.file_save(path, data)
                self.update_pb(file_count, i, path)


# sh4path = r"C:\GOG\Silent Hill 4\data"
# headers = set()
# headers2 = set()
#
# for file in os.listdir(sh4path):
#
#     with open(f"{sh4path}\\{file}", 'rb') as f:
#         h = int.from_bytes(f.read(4), byteorder="little")
#         h2 = int.from_bytes(f.read(4), byteorder="little")
#         # print(file, h, h2)
#         count = headers.add(h)
#
#         headers2.add(h2)
#
#
# pprint([headers, len(headers)])
# pprint([headers2, len(headers2)])