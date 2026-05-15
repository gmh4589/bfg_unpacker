
from source.reaper import Reaper, file_reaper
from collections import namedtuple


class Nosferatu(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as f:
            magic = f.read(4)

            if not self.magic([b'GEEK', ], magic, 'Nosferatu The Wrath of Malachi'):
                return

            file_count = int.from_bytes(f.read(4), byteorder='little')/0x90
            f.seek(8, 1)
            FileData = namedtuple('FileData', ['file_offset', 'file_size', 'file_name'])
            file_data = []

            for i in range(file_count):
                file_data.append(
                    FileData(
                        file_offset=int.from_bytes(f.read(4), byteorder='little'),
                        file_size=int.from_bytes(f.read(4), byteorder='little'),
                        file_name=f.read(0x80).rstrip(b'\x00').decode('utf-8')
                    )
                )
            
            for i, data in enumerate(file_data):
                f.seek(data.file_offset)
                output_path = f"{self.output_folder}\\{data.file_name}"
                file_data = f.read(data.file_size)

                with open(output_path, 'wb') as new_file:
                    new_file.write(file_data)

                self.update_pb(file_count, i, data.file_name)
