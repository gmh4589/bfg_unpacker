import os
import zlib
from collections import namedtuple

from source.reaper import Reaper, file_reaper


class TruckSym(Reaper):

    @file_reaper
    def run(self):
        # TODO: Files without names!!! However, there have programs, with can saving files with names

        with open(self.file_name, "rb") as file:
            magic = file.read(12)

            if not self.magic([b'SCS#\x01\0\0\0CITY', ], magic, 'DAT'):
                return

            file_count = int.from_bytes(file.read(4), byteorder="little")
            start_data = int.from_bytes(file.read(4), byteorder="little")
            file.seek(start_data)
            FileList = namedtuple("FileList",
                                   ['hash_1', 'offset', 'file_type', 'hash_2', 'size', 'z_size'])
            file_list = []

            for i in range(file_count):
                file_list.append(
                    FileList(
                        file.read(8),                                      # Hash 1
                        int.from_bytes(file.read(8), byteorder="little"),  # Offset
                        int.from_bytes(file.read(4), byteorder="little"),  # File Type
                        file.read(4),                                      # Hash 2
                        int.from_bytes(file.read(4), byteorder="little"),  # Size
                        int.from_bytes(file.read(4), byteorder="little")   # Zipped Size
                    )
                )

            for j, f in enumerate(file_list):
                file.seek(f.offset)
                data = file.read(f.size)

                if f.size > f.z_size:
                    data = zlib.decompress(data)

                name = f"{j:05}.{self.get_ext(data[:4])}"
                path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as new_file:
                    new_file.write(data)

                self.update_pb(file_count, j + 1, name)
