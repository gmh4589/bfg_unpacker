import bz2
import zlib
# import lzma
import os
# import zipfile
from source.reaper import Reaper, file_reaper
from source.ui import localize


# class Zip(Reaper):
#
#     @file_reaper
#     def run(self):
#
#         with zipfile.ZipFile(self.file_name, mode="r") as archive:
#             # archive.extractall(self.output_folder)
#             a = len(archive.namelist())
#             for i, file in enumerate(archive.infolist()):
#                 print(f"Saving - {file.filename}...")
#                 self.update_signal.emit(int((100 / a) * i), f'{i + 1}/{a}%', f'Saving - {file.filename}...', False)
#                 archive.extract(file, self.output_folder)
#
#         self.update_signal.emit(100, '', 'Done!', True)


class Zip(Reaper):

    @file_reaper
    def run(self):

        def write_file(p, cm, cd, percent):

            if p[-1] == '/':
                os.makedirs(p, exist_ok=True)
            else:

                with open(p, 'wb') as new_file:

                    if cm == b'\x00\x00':
                        new_file.write(cd)
                    elif cm == b'\x08\x00':  # Deflate
                        new_file.write(zlib.decompress(cd, -zlib.MAX_WBITS))
                    # elif cm in (b'\x09\x00', ):  # Deflate 64
                    #     pass
                    # elif cm in (b'\x0a\x00', ):  # PKWare
                    #     pass
                    elif cm == b'\x0c\x00':  # BZIP2
                        new_file.write(bz2.decompress(cd))
                    # elif cm == b'\x0e\x00':  # LZMA
                        # new_file.write(lzma.decompress(cd))
                    # elif cm in (b'\x12\x00', ):  # IBM TERSE
                    #     pass
                    # elif cm in (b'\x13\x00', ):  # LZ77
                    #     pass
                    # elif cm in (b'\x61\x00', ):  # WavPack
                    #     pass
                    # elif cm in (b'\x62\x00', ):  # PPMD
                    #     pass
                    else:
                        new_file.write(cd)
                        print(localize.not_unzipped)

                print(f"{localize.saving} - {p}...")
                self.update_signal.emit(percent, f'{percent}%', f'{localize.saving} - {p}...', False)

        size = os.path.getsize(self.file_name)

        with open(self.file_name, 'rb') as data:

            while True:

                pp = int((100 / size) * data.tell())
                magic = data.read(4)

                if magic == b'PK\x03\x04':
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
                    write_file(path, compress_method, compressed_data, pp)

                elif magic in (b'PK\x05\x06', b'PK\x01\x02'):
                    break

                else:
                    print(localize.not_correct_file)
                    break

            self.update_signal.emit(100, '', localize.done, True)
