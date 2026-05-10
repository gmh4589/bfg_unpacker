import bz2
import zlib
import os

from icecream import ic
from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.codecs.zip_methods import ZipMethods
from source.codecs.oodle import OodleDecompress

DEBUG = False

# TODO: Add support other compress codecs

#  Other methods:
#  1 - shrink +
#  2 - reduce1 +
#  3 - reduce2 +
#  4 - reduce3 +
#  5 - reduce4 +
#  8 - Deflate +
#  9 - deflate64 +
#  6, 10 - PKWare +
#  12 - BZIP +
#  13, 21 - XMemDecompress -
#  14 - lzma +
#  15 - oodle +
#  18 - terse +
#  19 - LZ77 +
#  20, 93 - ZSTD +
#  24 - lzma86dechead +
#  28 - LZ4F +
#  34 - broti +
#  64 - darksector +
#  94 - MP3 -
#  95 - LZMA2_EFS0 + ?
#  95 - XZ - ?
#  96 - jpeg
#  97 - WavPack
#  98 - ppmd +
#  99 - lzfse +


class ZipData:
    version: bytes
    flags: bytes
    compress_method: int
    date_time: bytes
    crc32: bytes
    compressed_size: int
    uncompressed_size: int
    file_name_long: int
    additional_field_long: int
    file_name: str
    additional_field: bytes
    compressed_data: bytes
    path: str


class Zip(Reaper):
    zip_data = ZipData()
    oodle = OodleDecompress()

    def write_file(self):
        cd = self.zip_data.compressed_data
        cm = self.zip_data.compress_method
        path = self.zip_data.path

        if cm == 8:

            try:
                cd = zlib.decompress(cd, -zlib.MAX_WBITS)
            except zlib.error:
                cm = 8000

        elif cm == 12:
            cd = bz2.decompress(cd)
        elif cm == 15:
            cd = self.oodle.decompress(cd)

        self.file_save(path, cd)

        if cm == 1:  # Shrink
            self.unzip(path, ZipMethods.SHRINK)

        elif cm == 2:  # reduce1
            self.unzip(path, ZipMethods.REDUCE1)

        elif cm == 3:  # reduce2
            self.unzip(path, ZipMethods.REDUCE2)

        elif cm == 4:  # reduce3
            self.unzip(path, ZipMethods.REDUCE3)

        elif cm == 5:  # reduce4
            self.unzip(path, ZipMethods.REDUCE4)

        elif cm == 6:  # Imploded
            self.unzip(path, ZipMethods.WINIMPLODE)

        elif cm == 9:  # Deflate 64
            self.unzip(path, ZipMethods.DEFLATE64)

        elif cm in (10, 11, 13, 15, 17):  # PKWare
            self.unzip(path, ZipMethods.PKWARE_DCL)

        elif cm == 14:  # LZMA
            self.unzip(path, ZipMethods.LZMA_DYNAMIC)

        elif cm == 18:  # Terse
            self.unzip(path, ZipMethods.TERSE)

        elif cm == 19:  # LZ77
            self.unzip(path, ZipMethods.LZ77_0)

        elif cm in (20, 93):  # ZSTD
            self.unzip(path, ZipMethods.ZSTD)

        elif cm == 24:  # LZMA86_Dechead
            self.unzip(path, ZipMethods.LZMA_86DECHEAD)

        elif cm == 28:  # LZ4F
            self.unzip(path, ZipMethods.LZ4F)

        elif cm == 64:  # darksector
            self.unzip(path, ZipMethods.DARKSECTOR)

        elif cm == 95:  # LZMA2_EFS0
            self.unzip(path, ZipMethods.LZMA2_EFS0)

        elif cm == 98:  # PPMD
            self.unzip(path, ZipMethods.PPMDI)

        elif cm == 99:  # LZFSE
            self.unzip(path, ZipMethods.LZFSE)
        
        elif cm == 8000:  # Raw Deflate
            self.unzip(path, ZipMethods.ZLIB_NOERROR)

        elif cm in (8, 12, 15):
            pass

        else:
            print(localize.not_unzipped)

    @file_reaper
    def run(self):
        size = os.path.getsize(self.file_name)

        with open(self.file_name, 'rb') as data:

            while True:

                pp = int((100 / size) * data.tell())
                magic = data.read(4)

                if magic in (b'PK\x03\x04', ):
                    self.zip_data.version = data.read(2)
                    self.zip_data.flags = data.read(2)
                    self.zip_data.compress_method = int.from_bytes(data.read(2), byteorder="little")
                    self.zip_data.date_time = data.read(4)
                    self.zip_data.crc32 = data.read(4)
                    self.zip_data.compressed_size = int.from_bytes(data.read(4), byteorder="little")
                    self.zip_data.uncompressed_size = int.from_bytes(data.read(4), byteorder="little")
                    self.zip_data.file_name_long = int.from_bytes(data.read(2), byteorder="little")
                    self.zip_data.additional_field_long = int.from_bytes(data.read(2), byteorder="little")
                    self.zip_data.file_name = data.read(self.zip_data.file_name_long).decode("utf-8")
                    self.zip_data.additional_field = data.read(self.zip_data.additional_field_long)
                    self.zip_data.compressed_data = data.read(self.zip_data.compressed_size)
                    self.zip_data.path = f"{self.output_folder}\\{self.zip_data.file_name}"

                    if self.zip_data.path[-1] != '/':
                        self.write_file()

                elif magic in (b'PK\x07\x08', ):
                    data.seek(12, 1)
    
                elif magic in (b'PK\x05\x06', b'PK\x01\x02', ):
                    self.update_signal.emit(100, '', localize.done, True)
                    break

                elif magic in (b'\xf8\x0f\x00\x00', ):
                    # Skip APK debug block
                    ic('APK debug block find...')
                    data.seek(0x1000 - 4, 1)

                elif not magic:
                    self.update_signal.emit(100, '', localize.eof_data, True)
                    print(localize.eof_data)
                    break

                else:
                    if DEBUG:
                        ic(magic, hex(data.tell()))
                        ic('Detected archive without file sizes...')

                    if self.zip_data.compressed_size == 0:
                        here = data.tell()
                        temp_data = data.read().split(b'PK\x07\x08')[0]
                        data.seek(here + len(temp_data))
                        self.zip_data.compressed_data = magic + temp_data
                        self.write_file()

                print(f"{localize.saving} - {self.zip_data.file_name}...")
                self.update_signal.emit(pp, f'{pp}%', f'{localize.saving} - {self.zip_data.file_name}...', False)

            self.update_signal.emit(100, '', localize.done, True)
