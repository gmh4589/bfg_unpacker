from collections import namedtuple
from icecream import ic

from source.reaper import Reaper, file_reaper


class Gothic(Reaper):
    # TODO: Need add TEX to DDS converter

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as vdf:
            magic = vdf.read(4)

            if not self.magic([b'Goth', ], magic, 'Gothic 1 Classic'):
                return

            vdf.seek(0x110)
            file_count = int.from_bytes(vdf.read(4), 'little')
            vdf.seek(0x128)

            FileData = namedtuple('FilaData',
                                  ['name', 'offset', 'size'])
            file_data = []

            for _ in range(file_count):
                file_data.append(
                    FileData(
                        name=vdf.read(0x40).decode('utf-8', errors='ignore').strip(),
                        offset=int.from_bytes(vdf.read(4), 'little'),
                        size=int.from_bytes(vdf.read(4), 'little')
                    )
                )
                vdf.seek(8, 1)

            for i, f in enumerate(file_data):

                if f.size:
                    vdf.seek(f.offset)
                    data = vdf.read(f.size)
                    self.file_save(f"{self.output_folder}\\{f.name}", data)

                self.update_pb(file_count, i + 1, f.name)
                
