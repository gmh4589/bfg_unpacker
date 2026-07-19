import os
from collections import namedtuple

from source.reaper import Reaper, file_reaper


class HOMM(Reaper):

    @file_reaper
    def run(self):
        ext = self.file_name.split('.')[-1].lower()

        FileList = namedtuple('FileList',
                              ['name', 'offset', 'size'])
        file_list = []

        with open(self.file_name, 'rb') as homm:
            file_count = int.from_bytes(homm.read(4), 'little')
            file_size = os.path.getsize(self.file_name)

            for _ in range(file_count):
                file_list.append(
                    FileList(
                        name=homm.read(0x28).strip(b'\0').replace(b'\0', b'.').decode('utf-8', errors='ignore'),
                        offset=int.from_bytes(homm.read(4), 'little'),
                        size=0 if ext == 'vid' else int.from_bytes(homm.read(4), 'little'),
                    )
                )
            
            for i, file in enumerate(file_list):
                homm.seek(file.offset)

                try:
                    size = file.size if file.size != 0 else file_list[i + 1].offset - file.offset
                except IndexError:
                    size = file.size if file.size != 0 else file_size - file.offset

                data = homm.read(size)
                self.file_save(f"{self.output_folder}\\{file.name}", data)
                self.update_pb(file_count, i + 1, file.name)

