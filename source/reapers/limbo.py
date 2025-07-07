import os
import zlib
import io
from PIL import Image
from collections import namedtuple
from source.reaper import Reaper, file_reaper


class LimboPKG(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as pkg_file:

            file_count = int.from_bytes(pkg_file.read(4), byteorder="little")
            FileList = namedtuple('FileList',
                                  ['hash_sum', 'file_start', 'file_long'])
            file_list = []
            os.makedirs(self.output_folder + '\\scripts', exist_ok=True)

            for i in range(file_count):
                file_list.append(
                    FileList(
                        int.from_bytes(pkg_file.read(4), byteorder="little"),
                        int.from_bytes(pkg_file.read(4), byteorder="little"),
                        int.from_bytes(pkg_file.read(4), byteorder="little")
                    )
                )

            for j, file in enumerate(file_list):
                name = f'\\scripts\\{file.hash_sum}.dat'
                path = self.output_folder + name
                data = pkg_file.read(file.file_long)

                try:
                    data = zlib.decompress(data)
                    new_data = io.BytesIO(data)
                    ident = int.from_bytes(new_data.read(4), byteorder="little")

                    if ident == 9:
                        new_data.seek(0xc, 1)
                        name_long = int.from_bytes(new_data.read(1))
                        name = new_data.read(name_long).decode('utf-8', errors='ignore')
                        path = self.output_folder + f'\\{name}'
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        new_data.seek(6, 1)
                        width = int.from_bytes(new_data.read(2), byteorder="little")
                        height = int.from_bytes(new_data.read(2), byteorder="little")
                        new_data.seek(8, 1)
                        data = Image.frombytes('LA', (width, height), new_data.read())
                        data.save(path)
                        data = b''

                except zlib.error:
                    pass

                if data:
                    self.file_save(path, data)

                self.update_pb(file_count, j + 1, name)
