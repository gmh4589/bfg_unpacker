import os
from collections import namedtuple
from io import BytesIO
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.ui import localize


class PKGExtractor(Reaper):

    DatasList = namedtuple('DatasList',
                           ['FileName', 'UnzipSize', 'ZipSize', 'Offset', 'Zipped'])

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as pkg_read:
            magic = pkg_read.read(4)

            if magic != b'\0' * 4:
                print(localize.not_correct_file.replace('%%', 'Trails of Cold Steal'))
                self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'Trails of Cold Steal'), True)
                return

            file_count = int.from_bytes(pkg_read.read(4), byteorder='little')
            data_list = []

            for _ in range(file_count):
                file_name = pkg_read.read(64).decode('utf-8').strip('\x00')
                unzipped_size = int.from_bytes(pkg_read.read(4), byteorder='little')
                size = int.from_bytes(pkg_read.read(4), byteorder='little')
                offset = int.from_bytes(pkg_read.read(4), byteorder='little')
                zipped = bool.from_bytes(pkg_read.read(4), byteorder='little')
                data_list.append(self.DatasList(file_name, unzipped_size, size, offset, zipped))

            for i, file_data in enumerate(data_list):
                pkg_read.seek(file_data.Offset, 0)

                if not file_data.Zipped:
                    data = pkg_read.read(file_data.UnzipSize)
                else:
                    new_stream = BytesIO()
                    pkg_read.seek(8, 1)
                    key = int.from_bytes(pkg_read.read(4), byteorder='little')

                    while new_stream.tell() < file_data.UnzipSize:
                        byte = int.from_bytes(pkg_read.read(1), byteorder='little')

                        if byte == key:
                            next_byte = int.from_bytes(pkg_read.read(1), byteorder='little')

                            if next_byte == key:
                                new_stream.write(bytes([next_byte]))
                            else:

                                if next_byte >= key:
                                    next_byte -= 1

                                position = new_stream.tell() - next_byte
                                count = int.from_bytes(pkg_read.read(1), byteorder='little')
                                current_position = new_stream.tell()
                                new_stream.seek(position)
                                buffer = new_stream.read(count)
                                new_stream.seek(current_position)
                                new_stream.write(buffer)
                        else:
                            new_stream.write(bytes([byte]))

                    data = new_stream.getvalue()

                os.makedirs(self.output_folder, exist_ok=True)

                with open(os.path.join(self.output_folder, file_data.FileName), 'wb') as new_file:
                    new_file.write(data)
                    ic(file_data.FileName)
                    print(f'{localize.saving}: {file_data.FileName}...')
                    self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                            f'{localize.saving} - {file_data.FileName}...', False)

            self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
