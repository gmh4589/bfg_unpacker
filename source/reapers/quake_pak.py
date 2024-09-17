
import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class QPAKExtractor(Reaper):

    def __init__(self, version=0):
        super().__init__()
        self.version = version

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as pak_file:
            magic = pak_file.read(4)

            if magic != b'PACK':
                print(localize.not_correct_file.replace('%%', 'PAK'))
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'PAK'), True)
                return

            entry_offset = int.from_bytes(pak_file.read(4), byteorder="little")
            long = int.from_bytes(pak_file.read(4), byteorder="little")

            pak_file.seek(entry_offset)
            file_list = {}
            file_size = os.path.getsize(self.file_name)

            while True:

                try:
                    name = pak_file.read(56).decode("ascii").rstrip("\0").replace("\0", '.')
                    i = 0
                except UnicodeDecodeError:
                    # TODO: Localize text!!!
                    print('You select invalid version, select other version!')
                    i = -1
                    break

                offset = int.from_bytes(pak_file.read(4), byteorder="little")
                size = int.from_bytes(pak_file.read(4), byteorder="little")
                file_list[name] = [offset, size]

                if self.version == 2:
                    pak_file.seek(8, 1)

                if pak_file.tell() >= file_size:
                    break

            if i >= 0:

                for name, value in file_list.items():
                    i += 1
                    offset, size = value
                    path = os.path.join(self.output_folder, name)
                    ic(path)
                    os.makedirs(os.path.dirname(path), exist_ok=True)

                    with open(path, 'wb') as new_file:
                        pak_file.seek(offset)
                        new_file.write(pak_file.read(size))

                    self.update_pb(len(file_list), i, name)
