import bz2
import zlib
import lzma
import os
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize
# TODO: Add support other compress codecs

#  Other methods:
#  1 - shrink +
#  2 - reduce1 +
#  3 - reduce2 +
#  4 - reduce3 +
#  5 - reduce4 +
#  9 - deflate64 +
#  6, 10 - pkware +
#  13, 21 - XMemDecompress
#  14 - lzma +
#  15 - oodle +
#  18 - terse +
#  19 - LZ77 +
#  20 - ZSTD +
#  24 - lzma86dechead +
#  28 - LZ4F +
#  34 - broti +
#  64 - darksector +
#  93 - ZSTD +
#  95 - LZMA2_EFS0 +
#  96 - jpeg
#  97 - wavpack
#  98 - ppmd +
#  99 - lzfse +


class Zip(Reaper):

    def write_file(self, path, cm, cd):
        cm = int.from_bytes(cm, byteorder='little')

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as new_file:

            if cm == 0:
                new_file.write(cd)

            elif cm == 8:  # Deflate
                new_file.write(zlib.decompress(cd, -zlib.MAX_WBITS))

            elif cm == 12:  # BZIP2
                new_file.write(bz2.decompress(cd))

            else:
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

        elif cm == 6:  # Imploded
            self.unzip(path, 675)

        elif cm == 9:  # Deflate 64
            self.unzip(path, 79)

        elif cm in (10, 11, 13, 15, 17):  # PKWare
            self.unzip(path, 618)

        elif cm == 14:  # LZMA
            self.unzip(path, 295)

        elif cm == 15:  # Oodle
            self.unzip(path, 650)

        elif cm == 18:  # Terse
            self.unzip(path, 619)

        elif cm == 19:  # LZ77
            self.unzip(path, 199)

        elif cm in (20, 93):  # ZSTD
            self.unzip(path, 478)

        elif cm == 24:  # LZMA86_Dechead
            self.unzip(path, 19)

        elif cm == 28:  # LZ4F
            self.unzip(path, 429)

        elif cm == 64:  # darksector
            self.unzip(path, 60)

        elif cm == 95:  # LZMA2_EFS0
            self.unzip(path, 454)

        elif cm == 98:  # PPMD
            self.unzip(path, 81)

        elif cm == 99:  # LZFSE
            self.unzip(path, 667)

        elif cm in (0, 8, 12, 14):
            pass

        else:
            print(localize.not_unzipped)
            cm = [cm, -1]

        return cm

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
                    compress_method = data.read(2)
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

                    if path[-1] == '/':
                        os.makedirs(path, exist_ok=True)
                    else:
                        output_code = self.write_file(path, compress_method, compressed_data)
                        ic(f"Output code: {output_code}")

                elif magic in (b'PK\x07\x08', ):
                    data.seek(12, 1)
    
                elif magic in (b'PK\x05\x06', b'PK\x01\x02', ):
                    self.update_signal.emit(100, '', localize.done, True)
                    break

                elif magic in (b'\xf8\x0f\x00\x00', ):
                    # Skip APK debug block
                    ic('APK debug block find...')
                    data.seek(0x1000 - 4, 1)

                else:
                    ic(magic)
                    self.update_signal.emit(100, '', 'Find data after EOF signature', True)
                    print('Find data after EOF signature')
                    break

                print(f"{localize.saving} - {file_name}...")
                self.update_signal.emit(pp, f'{pp}%', f'{localize.saving} - {file_name}...', False)

            self.update_signal.emit(100, '', localize.done, True)
