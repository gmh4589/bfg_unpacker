
import os
from source.reaper import Reaper, file_reaper


class AFS2Extractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as afs_file:
            magic = afs_file.read(4)

            if not self.magic([b'AFS2', ], magic, 'AWB'):
                return

            afs_file.seek(8)
            file_count = int.from_bytes(afs_file.read(4), byteorder="little")
            afs_file.seek(4 + file_count * 2, 1)
            rd = 4 if os.path.getsize(self.file_name) > 0xFFFF else 2

            for i in range(file_count):
                name = f"{self.output_folder}\\{str(i).rjust(8, '0')}.dat"
                offset = int.from_bytes(afs_file.read(rd), byteorder="little")
                here = afs_file.tell()
                next_offset = int.from_bytes(afs_file.read(rd), byteorder="little") 
                size = next_offset - offset
                print(size, offset, next_offset)
                afs_file.seek(offset)
                data = afs_file.read(size)
                self.file_save(name, data)
                self.update_pb(file_count, i + 1, name)
                afs_file.seek(here)


