import os
from source.reaper import Reaper, file_reaper


class Indiana(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as res_file:
            magic = res_file.read(4)

            if not self.magic([b'IDCL', ], magic, 'idTech 7'):
                return

            version = int.from_bytes(res_file.read(4), byteorder="little")
            hash_sum = int.from_bytes(res_file.read(8), byteorder="little")
            res_file.seek(0x44)
            file_data_start = int.from_bytes(res_file.read(8), byteorder="little")
            file_data_end = int.from_bytes(res_file.read(8), byteorder="little")
            res_file.seek(file_data_start)
            file_count = int.from_bytes(res_file.read(8), byteorder="little")
            names_offsets = []

            for i in range(file_count):
                name_start = int.from_bytes(res_file.read(8), byteorder="little")
                names_offsets.append(name_start)

            names_offsets.append(file_data_end - res_file.tell())

            for j in range(file_count):
                name_len = names_offsets[j + 1] - names_offsets[j]
                name = res_file.read(name_len).strip(b'\0').decode('utf-8')

                if '.' in name:
                    print(name)

                # self.update_pb(file_count, j + 1, name)
