import os
import zlib

from source.reaper import Reaper, file_reaper
from source.ui import localize


class ArcanumDAT(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(2)

            if not self.magic([b'\x78\xDA', ], magic, 'Arcanum DAT'):
                return

            file_size = len(file.read()) + 2
            file.seek(file_size - 4)
            list_len = int.from_bytes(file.read(4), byteorder="little")
            file.seek(file_size - list_len)
            file_count = int.from_bytes(file.read(4), byteorder="little")
            print(list_len, file_count)

            for i in range(file_count):
                name_len = int.from_bytes(file.read(4), byteorder="little")
                name = file.read(name_len).decode("ascii").rstrip("\0")
                file.seek(8, 1)
                unzip_size = int.from_bytes(file.read(4), byteorder="little")
                zip_size = int.from_bytes(file.read(4), byteorder="little")
                start_data = int.from_bytes(file.read(4), byteorder="little")
                here = file.tell()

                if unzip_size > 0:
                    file.seek(start_data)
                    output_path = os.path.join(self.output_folder, name)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    file_data = file.read(zip_size)

                    if unzip_size != zip_size:
                        file_data = zlib.decompress(file_data)

                    with open(f"{self.output_folder}/{name}", "wb") as out:
                        out.write(file_data)

                file.seek(here)
                self.update_pb(file_count, i + 1, name)

        self.update_signal.emit(100, '', localize.done, True)
