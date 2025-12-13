
from source.reaper import Reaper, file_reaper
import os
from collections import namedtuple


class BINExtractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bin_file:

            file_size = os.path.getsize(self.file_name)
            file_count = int.from_bytes(bin_file.read(4), byteorder="little")
            offsets = []

            for _ in range(file_count):
                offsets.append(int.from_bytes(bin_file.read(4), byteorder="little"))

            offsets.append(file_size)

            for i in range(file_count):
                bin_file.seek(offsets[i])
                data = bin_file.read(offsets[i + 1] - offsets[i])
                path = f"{self.output_folder}\\{os.path.basename(self.file_name)}_{i}.dat"
                self.file_save(path, data)
                self.update_pb(file_count, i, path)

      
class SH4Extractor(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as sh4_file:
            magic = sh4_file.read(4)

            if not self.magic([b'SH4\0', b'SDPA'], magic, 'Silent Hill 4: The Room SH4 File'):
                return
            
            file_count = int.from_bytes(sh4_file.read(4), byteorder="little")
            FileDataSH4 = namedtuple('FileData', ['offset', 'size'])
            FileDataPac = namedtuple('FileData', ['offset', 'size', 'nothing'])
            file_data = []
            base_name = os.path.splitext(os.path.basename(self.file_name))[0]

            for _ in range(file_count):

                if magic == b'SH4\0':
                    file_data.append(
                        FileDataSH4(
                            int.from_bytes(sh4_file.read(4), byteorder="little"), # Offset
                            int.from_bytes(sh4_file.read(4), byteorder="little")  # File Size
                        )
                    )
                else:
                    file_data.append(
                        FileDataPac(
                            int.from_bytes(sh4_file.read(4), byteorder="little"), # Offset
                            int.from_bytes(sh4_file.read(4), byteorder="little"), # File Size
                            int.from_bytes(sh4_file.read(4), byteorder="little")  # Nothing
                        )
                    )
            
            for i, file in enumerate(file_data):

                if file.size:
                    sh4_file.seek(file.offset)
                    file_data = sh4_file.read(file.size)
                    ext = self.get_ext(file_data[:4])
                    file_name = f'{base_name}_{i}.{ext}'
                    path = f'{self.output_folder}\\{file_name}'
                    self.file_save(path, file_data)
                    self.update_pb(file_count, i, file_name)

