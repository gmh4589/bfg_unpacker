from collections import namedtuple

from icecream import ic
from source.reaper import Reaper, file_reaper


class SPBUnpack(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            a = file.tell()
            magic = file.read(4)

            if not self.magic([b"\1\0\0\0", ], magic, 'Chrome Engine Archive'):
                return
            
            file.seek(0x8)
            file_count = int.from_bytes(file.read(4), byteorder="little")
            unk2 = int.from_bytes(file.read(4), byteorder="little")

            FileList = namedtuple('FileList', ['offset', 'size', 'file_name'])
            file_list = []

            for _ in range(file_count):
                file.seek(4, 1)
                file_list.append(
                    FileList(
                        offset = int.from_bytes(file.read(4), byteorder="little"),
                        size = int.from_bytes(file.read(8), byteorder="little"),
                        file_name = file.read(0x40).rstrip(b'\x00').decode('utf-8')
                        )
                    )
            
            for i, f in enumerate(file_list):
                file.seek(f.offset)
                data = file.read(f.size)
                full_name = f"{self.output_folder}\\{f.file_name}.dat"
                self.file_save(full_name, data)
                self.update_pb(file_count, i + 1, f.file_name)

