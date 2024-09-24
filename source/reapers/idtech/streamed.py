import os

from source.reaper import Reaper, file_reaper


class Streamed(Reaper):
    # For *.streamed from The Evil Within

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as streamed:
            magic = streamed.read(4)

            if not self.magic([b'\x23\x94\xAB\xCD', ], magic, 'idTech streamed'):
                return

            file_list_start = int.from_bytes(streamed.read(4), byteorder='big')
            streamed.seek(file_list_start + 0x14)
            file_list_len = int.from_bytes(streamed.read(4), byteorder='big')
            file_count = int.from_bytes(streamed.read(4), byteorder='big')
            file_list = [name.decode('utf-8', errors='ignore') for name in streamed.read(file_list_len).split(b'\0')]

            for file in file_list:
                i = int.from_bytes(streamed.read(4), byteorder='big')
                offset = int.from_bytes(streamed.read(4), byteorder='big')
                zip_size = int.from_bytes(streamed.read(4), byteorder='big')
                unzip_size = int.from_bytes(streamed.read(4), byteorder='big')
                here = streamed.tell()

                streamed.seek(offset)
                data = streamed.read(zip_size)
                path = os.path.join(self.output_folder, file_list[i])
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as nf:
                    nf.write(data)

                streamed.seek(here)
                self.update_pb(file_count, i + 1, file)
