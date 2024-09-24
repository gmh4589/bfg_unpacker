import os
from collections import namedtuple
import numpy
import io

from source.reaper import Reaper, file_reaper
# TODO: Add to archive creation support


class RFFExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as rff_file:
            magic = rff_file.read(4)

            if not self.magic([b"RFF\x1A", ], magic,  'Build Engine'):
                return

            FileList = namedtuple('FileList',
                                  ['name', 'size', 'offset'])
            file_list = []
            file_len = os.path.getsize(self.file_name)
            version = int.from_bytes(rff_file.read(4), byteorder="little")
            file_list_start = int.from_bytes(rff_file.read(4), byteorder="little")
            file_count = int.from_bytes(rff_file.read(4), byteorder="little")
            encryption = False if version == 0x200 else True
            file_list_len = file_len - file_list_start
            rff_file.seek(file_list_start)

            if encryption:

                key = file_list_start & 0xFF
                fat = bytearray(rff_file.read(file_list_len))
                fat = numpy.array(fat, dtype=numpy.uint8)

                for i in range(file_list_len):

                    if version == 0x300:
                        fat[i] ^= (key >> 1)
                        key += 1
                    else:
                        fat[i] ^= key
                        key += (i & 1)

                files_data = io.BytesIO(fat.tobytes())
                file_list_len = len(fat)

                with open('temp.dat', 'wb') as temp:
                    temp.write(fat.tobytes())

            else:
                files_data = io.BytesIO(rff_file.read(file_list_len))

            for j in range(file_list_len):
                files_data.seek(16, 1)
                offset = int.from_bytes(files_data.read(4), byteorder="little")
                size = int.from_bytes(files_data.read(4), byteorder="little")
                files_data.seek(9, 1)
                ext = files_data.read(3).decode('ascii')
                name = files_data.read(8).decode("ascii").split("\0")[0]
                files_data.seek(4, 1)
                file_list.append(FileList(f"{name}.{ext}", size, offset))

            for k, file in enumerate(file_list):
                rff_file.seek(file.offset)
                self.update_pb(file_count - 1, k, file.name)

                if k == file_count - 1:
                    return

                with open(os.path.join(self.output_folder, file.name), 'wb') as new_file:
                    new_file.write(rff_file.read(file.size))
