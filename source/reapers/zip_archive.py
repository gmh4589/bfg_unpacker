import bz2
import zlib
import os
# import zipfile
from source.reaper import Reaper


# class Zip(Reaper):
#
#     def run(self):
#
#         with zipfile.ZipFile(self.file_name, mode="r") as archive:
#             archive.extractall(self.output_folder)
#
#         self.update_signal.emit(100, '', 'Done!', True)
#


class Zip(Reaper):

    def run(self):

        def write_file(p, cm, cd):

            if p[-1] == '/':
                os.makedirs(p, exist_ok=True)
            else:

                with open(p, 'wb') as new_file:

                    if cm == b'\x0c\x00':
                        new_file.write(bz2.decompress(cd))
                    elif cm in (b'\x08\x00', ):
                        new_file.write(zlib.decompress(cd, -zlib.MAX_WBITS))
                    # elif cm in (b'\x08\x08', b'\x08\x09', b'\t\x00'):
                    #     pass
                    else:
                        new_file.write(cd)

                print(f"{cm} - {p}...")
                self.update_signal.emit(50, '', f'Saving - {p}...', False)

        with open(self.file_name, 'rb') as data:

            while True:

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
                    write_file(path, compress_method, compressed_data)

                elif magic in (b'PK\x05\x06', b'PK\x01\x02'):
                    break

                else:
                    print(f'Файл не является ZIP архивом! {data.tell()} {magic}')
                    break

            print('Done!')
            self.update_signal.emit(100, '', 'Done!', True)
