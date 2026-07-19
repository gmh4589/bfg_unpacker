import os
import zlib
from collections import namedtuple

from source.reaper import Reaper, file_reaper


class LOD(Reaper):

    @file_reaper
    def run(self):
        # TODO: Add PCX convert

        FileList = namedtuple('FileList',
                              ['name', 'offset', 'dummy', 'size', 'zip_size'])
        file_list = []

        with open(self.file_name, 'rb') as lod:
            lod.seek(8)
            file_count = int.from_bytes(lod.read(4), 'little')
            lod.seek(0x5C)

            for _ in range(file_count):
                file_list.append(
                    FileList(
                        name=lod.read(0x10).split(b'\0')[0].decode('utf-8', errors='ignore'),
                        offset=int.from_bytes(lod.read(4), 'little'),
                        dummy=int.from_bytes(lod.read(4), 'little'),
                        size=int.from_bytes(lod.read(4), 'little'),
                        zip_size=int.from_bytes(lod.read(4), 'little'),
                    )
                )
            
            for i, file in enumerate(file_list):
                lod.seek(file.offset)

                data = lod.read(file.zip_size if file.zip_size != 0 else file.size)

                if file.zip_size != 0:
                    data = zlib.decompress(data)

                self.file_save(f"{self.output_folder}\\{file.name}", data)
                self.update_pb(file_count, i + 1, file.name)

