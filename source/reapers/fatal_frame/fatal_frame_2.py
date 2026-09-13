
import os
from source.reaper import Reaper, file_reaper


class IMG_BDExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bin_file:
            magic = bin_file.read(4)

            if not self.magic([b'\x40\x04\x01\x00', ], magic, 'Fatal Frame 2 IMG_BD.BIN File'):
                return

            file_size = os.path.getsize(self.file_name)
            bin_file.seek(0)
            file_num = 0

            while bin_file.tell() < file_size:
                bin_file.seek(0x1c, 1)
                new_file_size = int.from_bytes(bin_file.read(4), byteorder='little')
                bin_file.seek(0x10, 1)
                file_data = bin_file.read(new_file_size)
                self.file_save(f"{self.output_folder}\\{file_num:08}.bin", file_data)
                file_num += 1

                while True:

                    if bin_file.read(1) != b'\0':
                        break

                bin_file.seek(bin_file.tell() - 1)

            self.update_pb(file_num, file_num, '')


