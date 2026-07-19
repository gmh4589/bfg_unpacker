from collections import namedtuple

from source.reaper import Reaper, file_reaper


class CSBUnpack(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            a = file.tell()
            magic = file.read(4)

            if not self.magic([b"\0\0\0\0", ], magic, 'Chrome Engine Archive'):
                return
            
            file.seek(0x44)
            file_count = int.from_bytes(file.read(4), byteorder="little")
            unk = int.from_bytes(file.read(4), byteorder="little")

            FileList = namedtuple('FileList', ['file_name', 'offset', 'size'])
            file_list = []

            for _ in range(file_count):
                file_list.append(
                    FileList(
                        file_name = file.read(0x40).rstrip(b'\x00').decode('utf-8'),
                        offset = int.from_bytes(file.read(4), byteorder="little"),
                        size = int.from_bytes(file.read(4), byteorder="little")
                        )
                    )
                file.seek(0x10, 1)
            
            for i, f in enumerate(file_list):
                file.seek(f.offset)
                data = file.read(f.size)
                full_name = f"{self.output_folder}\\{f.file_name}.fsb"
                self.file_save(full_name, data)
                self.update_pb(file_count, i + 1, f.file_name)

