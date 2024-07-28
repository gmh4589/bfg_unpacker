# import bz2
# import zlib
# import lzma
import os
# import zipfile
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize
# TODO: Add support other compress codecs


class Zip(Reaper):

    def write_file(self, path, cm, cd, percent):

        if path[-1] == '/':
            os.makedirs(path, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, 'wb') as new_file:
                new_file.write(cd)

            if cm == 1:  # Shrink
                self.unzip(path, 80)

            elif cm == 2:  # reduce1
                self.unzip(path, 622)

            elif cm == 3:  # reduce2
                self.unzip(path, 623)

            elif cm == 4:  # reduce3
                self.unzip(path, 624)

            elif cm == 5:  # reduce4
                self.unzip(path, 625)

            elif cm == 8:  # Deflate
                self.unzip(path, 171)

            elif cm == 9:  # Deflate 64
                self.unzip(path, 79)

            elif cm in (6, 10):  # PKWare
                self.unzip(path, 618)

            elif cm == 12:  # BZIP2
                self.unzip(path, 21)

            elif cm == 14:  # LZMA
                self.unzip(path, 295)

            elif cm == 15:  # Oodle
                self.unzip(path, 650)

            elif cm == 18:  # Terse
                self.unzip(path, 619)

            elif cm == 24:  # LZMA86_Dechead
                self.unzip(path, 19)

            elif cm == 28:  # LZ4F
                self.unzip(path, 429)

            elif cm == 64:  # LZ4F
                self.unzip(path, 60)

            elif cm == 95:  # LZMA2_EFS0
                self.unzip(path, 454)

            elif cm == 98:  # PPMD
                self.unzip(path, 81)

            elif cm == 99:  # LZMA2_EFS0
                self.unzip(path, 667)

            #  Other methods:
            #  13, 21 - XMemDecompress
            #  19 - LZ77
            #  34 - broti
            #  96 - jpeg
            #  97 - wavpack

            else:
                print(localize.not_unzipped)

            print(f"{localize.saving} - {path}...")
            self.update_signal.emit(percent, f'{percent}%', f'{localize.saving} - {path}...', False)

    @file_reaper
    def run(self):

        size = os.path.getsize(self.file_name)

        with open(self.file_name, 'rb') as data:

            while True:

                pp = int((100 / size) * data.tell())
                magic = data.read(4)

                if magic in b'PK\x03\x04':
                    version = data.read(2)
                    flags = data.read(2)
                    compress_method = int.from_bytes(data.read(2), byteorder="little")
                    date_time = data.read(4)
                    crc32 = data.read(4)
                    compressed_size = int.from_bytes(data.read(4), byteorder="little")
                    uncompressed_size = data.read(4)
                    file_name_long = int.from_bytes(data.read(2), byteorder="little")
                    additional_field_long = int.from_bytes(data.read(2), byteorder="little")
                    file_name = data.read(file_name_long).decode("utf-8")
                    additional_field = data.read(additional_field_long)
                    compressed_data = data.read(compressed_size)
                    path = os.path.join(self.output_folder, file_name)
                    self.write_file(path, compress_method, compressed_data, pp)

                elif magic in (b'PK\x05\x06', b'PK\x01\x02'):
                    self.update_signal.emit(100, '', localize.done, True)
                    break

                else:
                    ic(magic)
                    self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'ZIP'), True)
                    print(localize.not_correct_file.replace('%%', 'ZIP'))
                    break

            self.update_signal.emit(100, '', localize.done, True)
