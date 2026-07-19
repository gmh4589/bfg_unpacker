
from collections import namedtuple
import zlib

from source.reaper import Reaper, file_reaper


class DATExtractor(Reaper):

    def __init__(self):
        super().__init__()

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as dat_file:
            magic = dat_file.read(4)

            if not self.magic([b'ADAT'], magic, 'Anachronox DAT'):
                return

            start_data = int.from_bytes(dat_file.read(4), 'little')
            size_data = int.from_bytes(dat_file.read(4), 'little')
            file_count = int(size_data / 0x90)
            dat_file.seek(start_data)

            FileData = namedtuple('FileData',
                                  ['file_name', 'offset', 'unzip_size', 'zip_size', 'hash_sum'])
            file_data = []

            for _ in range(file_count):
                file_data.append(
                    FileData(
                        dat_file.read(0x80).decode('utf-8', errors='ignore').strip('\0'),
                        int.from_bytes(dat_file.read(4), 'little'),
                        int.from_bytes(dat_file.read(4), 'little'),
                        int.from_bytes(dat_file.read(4), 'little'),
                        int.from_bytes(dat_file.read(4), 'little'),
                    )
                )

            for i, f in enumerate(file_data):
                dat_file.seek(f.offset)
                data = dat_file.read(f.zip_size if f.zip_size else f.unzip_size)

                if f.zip_size > 0:
                    data = zlib.decompress(data)

                self.file_save(f"{self.output_folder}\\{f.file_name}", data)
                self.update_pb(file_count, i + 1, f.file_name)
