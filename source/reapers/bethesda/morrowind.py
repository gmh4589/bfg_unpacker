import os
from source.reaper import Reaper, file_reaper


class MorrowindBSA(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as bsa_file:
            magic = bsa_file.read(4)

            if not self.magic([b'\0\x01\0\0', ], magic, 'Bethesda Softworks Archive'):
                return

            long_data = int.from_bytes(bsa_file.read(4), byteorder="little")
            file_count = int.from_bytes(bsa_file.read(4), byteorder="little")
            offsets = []
            longs = []

            for i in range(file_count):
                long = int.from_bytes(bsa_file.read(4), byteorder="little")
                offset = int.from_bytes(bsa_file.read(4), byteorder="little")
                longs.append(long)
                offsets.append(offset)

            for _ in range(file_count):
                bsa_file.read(4)

            here = bsa_file.tell()

            pos = long_data - here + 12
            files_list = [file_name.decode('utf-8') for file_name in
                          bsa_file.read(pos).split(b'\0') if file_name]

            for _ in range(file_count):
                bsa_file.read(8)

            here = bsa_file.tell()

            for i, name in enumerate(files_list):
                bsa_file.seek(offsets[i] + here)
                data = bsa_file.read(longs[i])
                self.file_save(os.path.join(self.output_folder, name), data)
                self.update_pb(file_count, i, name)
