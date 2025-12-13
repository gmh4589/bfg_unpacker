
import os
from source.reaper import Reaper, file_reaper


class AFSExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as afs_file:
            magic = afs_file.read(4)

            if not self.magic([b'AFS\x00', ], magic, 'AFS'):
                return

            file_count = int.from_bytes(afs_file.read(4), byteorder="little")

            for i in range(file_count):
                name = str(i).rjust(8, '0') + '.dat'
                offset = int.from_bytes(afs_file.read(4), byteorder="little")
                size = int.from_bytes(afs_file.read(4), byteorder="little")

                path = f"{self.output_folder}\\{str(i).rjust(8, '0')}.dat"
                here = afs_file.tell()
                afs_file.seek(offset)
                data = afs_file.read(size)
                self.file_save(path, data)
                afs_file.seek(here)

                self.update_pb(file_count, i, name)
