
import os
from source.reaper import Reaper, file_reaper


class MorUnpacker(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as f:
            magic = f.read(4)

            if not self.magic([b'LP1C', ], magic, 'Pathologic Classic'):
                return

            f.seek(8)
            file_count = int.from_bytes(f.read(4), byteorder='little')

            for i in range(file_count):
                name_length = int.from_bytes(f.read(1), byteorder='little')
                name = f.read(name_length).decode('unicode_escape')
                file_position = f.tell()
                file_size = int.from_bytes(f.read(4), byteorder='little')
                file_offset = int.from_bytes(f.read(4), byteorder='little')
                f.seek(file_offset)
                file_data = f.read(file_size)
                output_path = os.path.join(self.output_folder, name)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as new_file:
                    new_file.write(file_data)

                f.seek(file_position + 16)
                self.update_pb(file_count, i, name)
