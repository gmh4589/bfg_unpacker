import os
import io
import struct
from source.reaper import Reaper, file_reaper


class MaxPayne(Reaper):
    testing = True

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)

            if not self.magic([b'RAS\0', ], magic, 'Max Payne Archive'):
                return

            # key = int.from_bytes(file.read(4), byteorder="little")
            key = file.read(4)
            key = struct.unpack('<i', key)[0]

            head_decrypted = self.ras_decrypt(bytearray(file.read(0x24)), key)
            file_count = int.from_bytes(head_decrypted[:4], byteorder="little")
            folder_count = int.from_bytes(head_decrypted[4:8], byteorder="little")
            file_long = int.from_bytes(head_decrypted[8:12], byteorder="little")
            folder_long = int.from_bytes(head_decrypted[12:16], byteorder="little")

            file_list_decrypted = self.ras_decrypt(bytearray(file.read(file_long)), key)
            folder_list_decrypted = self.ras_decrypt(bytearray(file.read(folder_long)), key)

            if self.testing:
                self.test_write(head_decrypted, 'head.dec')
                self.test_write(file_list_decrypted, 'file_list.dec')
                self.test_write(folder_list_decrypted, 'folder_list.dec')

            files_stream = io.BytesIO(file_list_decrypted)
            folders_stream = io.BytesIO(folder_list_decrypted)

            folder_list = []

            for _ in range(folder_count):
                here = (folders_stream.tell())
                folder_name = folders_stream.read(0x100).split(b'\0')[0]
                folder_name = folder_name.decode('utf-8', errors='ignore')
                folder_list.append(folder_name)
                move_to = here + len(folder_name) + 0x10 + 1
                folders_stream.seek(move_to)

            for f in range(file_count):
                here2 = files_stream.tell()
                file_name = files_stream.read(0x100).split(b'\0')[0]
                name_long = len(file_name)
                files_stream.seek(here2 + name_long + 1)
                files_stream.seek(4, 1)
                zip_size = int.from_bytes(files_stream.read(4), byteorder="little")
                files_stream.seek(4, 1)
                dir_index = int.from_bytes(files_stream.read(4), byteorder="little")
                files_stream.seek(24, 1)

                file_name = file_name.decode('utf-8', errors='ignore')
                path = self.output_folder + folder_list[dir_index] + file_name
                file_data = file.read(zip_size)

                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as nf:
                    nf.write(file_data)

                self.update_pb(file_count, f + 1, path)

    def test_write(self, data, f_name):
        f_name = self.output_folder + '\\' + f_name

        with open(f_name, 'wb') as nf:
            nf.write(data)

    @staticmethod
    def ras_decrypt(data: bytearray, seed: int):

        if seed == 0:
            seed = 1

        size = len(data)

        for i in range(size):
            seed = (seed * 0xAB) + (-0x763D * int(seed / 0xB1))
            data[i] = ((data[i] << (i % 5)) | (data[i] >> (8 - (i % 5)))) & 0xFF
            data[i] = ((((i + 3) * 6) ^ data[i]) + seed) & 0xFF

        return data
