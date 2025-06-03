import os
from source.reaper import Reaper, file_reaper


class OldBSA(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bsa_file:
            file_len = os.path.getsize(self.file_name)
            file_count = int.from_bytes(bsa_file.read(2), byteorder="little")
            key = int.from_bytes(bsa_file.read(2), byteorder="big")
            pos = 4 if key < 3 else 2

            file_list_start = (file_len - file_count * 0x12) if "ARCH3D" not in self.file_name else 0x19CED14
            bsa_file.seek(file_list_start)

            for i in range(file_count):
                name = (bsa_file.read(14)[:13].rstrip(b'\x00').decode('utf-8', errors='ignore')
                        if "ARCH3D" not in self.file_name else str(int.from_bytes(bsa_file.read(4), byteorder="little")))
                size = int.from_bytes(bsa_file.read(4), byteorder="little")
                here = bsa_file.tell()
                bsa_file.seek(pos)
                data = bsa_file.read(size)
                pos += size
                bsa_file.seek(here)

                if "ARCH3D" in self.file_name:
                    name += '.3D'

                self.file_save(os.path.join(self.output_folder, f"{name}"), data)
                self.update_pb(file_count, i, name)
