import os
from icecream import ic
from source.reaper import Reaper, file_reaper
from source.ui.localize import invalid_version


class QPAKExtractor(Reaper):

    def __init__(self):
        super().__init__()

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as pak_file:
            magic = pak_file.read(4)

            if not self.magic([b'PACK', b'SPAK'], magic, 'idTech 2'):
                return

            entry_offset = int.from_bytes(pak_file.read(4), byteorder="little")
            long = int.from_bytes(pak_file.read(4), byteorder="little") / 64

            pak_file.seek(entry_offset + 0x44)
            version = int.from_bytes(pak_file.read(4), byteorder="little")
            version = 2 if version in (0, 1) else 1
            version = 3 if magic == b'SPAK' else version
            pak_file.seek(entry_offset)

            file_list = {}

            for _ in range(int(long)):
                name = pak_file.read(0x78 if version == 3 else 0x38).split(b'\0')[0]

                try:
                    name = name.decode("ascii").rstrip("\0")
                except UnicodeDecodeError:
                    print(invalid_version)
                    self.update_pb(len(file_list), len(file_list), name)
                    break

                offset = int.from_bytes(pak_file.read(4), byteorder="little")
                size = int.from_bytes(pak_file.read(4), byteorder="little")
                file_list[name] = [offset, size]

                if version == 2:
                    pak_file.seek(8, 1)

            i = 0

            for name, value in file_list.items():

                if not name:
                    break

                i += 1
                offset, size = value
                pak_file.seek(offset)
                self.file_save(os.path.join(self.output_folder, name), pak_file.read(size))
                self.update_pb(len(file_list), i, name)
