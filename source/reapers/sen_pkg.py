import os
from collections import namedtuple, Counter
from io import BytesIO

from source.reaper import Reaper, file_reaper
from source.ui import localize


class PKGExtractor(Reaper):

    @file_reaper
    def run(self):

        DatasList = namedtuple('DatasList',
                               ['FileName', 'UnzipSize', 'ZipSize', 'Offset', 'Zipped'])

        with open(self.file_name, 'rb') as pkg_read:
            magic = pkg_read.read(4)

            file_count = int.from_bytes(pkg_read.read(4), byteorder='little')
            data_list = []

            for _ in range(file_count):
                file_name = pkg_read.read(64).decode('utf-8').strip('\x00')
                unzipped_size = int.from_bytes(pkg_read.read(4), byteorder='little')
                size = int.from_bytes(pkg_read.read(4), byteorder='little')
                offset = int.from_bytes(pkg_read.read(4), byteorder='little')
                zipped = bool.from_bytes(pkg_read.read(4), byteorder='little')
                data_list.append(DatasList(file_name, unzipped_size, size, offset, zipped))

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
                    print(f'{localize.saving}: {file_data.FileName}...')
                    self.update_signal.emit(int(100 / file_count * i), f'{i}/{file_count}',
                                            f'{localize.saving} - {file_data.FileName}...', False)

            self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)


class PKGPacker(Reaper):

    COMPRESSED = True

    @staticmethod
    def compress_data(data, flag_byte):
        compressed_stream = BytesIO()
        uncompressed_stream = BytesIO()
        buffer = b''

        for j, byte in enumerate(data):

            if byte == flag_byte:
                compressed_stream.write(buffer + bytes([byte, byte]))
                uncompressed_stream.write(buffer + bytes([byte]))
                buffer = b''
            else:
                buffer += byte.to_bytes(1)

                if j > len(buffer):

                    if len(buffer) > 4:
                        uncompressed_stream.seek(max(j - 256, 0))
                        zzz = uncompressed_stream.read()

                        if buffer not in zzz:

                            if buffer[:-1] in zzz:
                                index = len(zzz) - zzz.find(buffer[:-1])
                                index = index + (1 if flag_byte < index else 0) if index < 255 else 0

                                if index == flag_byte:
                                    compressed_stream.write(buffer)
                                else:
                                    compressed_stream.write(flag_byte.to_bytes(1) +
                                                            index.to_bytes(1) +
                                                            (len(buffer) - 1).to_bytes(1) +
                                                            buffer[-1].to_bytes(1))

                                uncompressed_stream.write(buffer)

                            else:
                                compressed_stream.write(buffer)
                                uncompressed_stream.write(buffer)

                            buffer = b''

                else:
                    compressed_stream.write(buffer)
                    uncompressed_stream.write(buffer)
                    buffer = b''

        compressed_stream.write(buffer)
        uncompressed_size = len(data)
        compressed_size = compressed_stream.tell() + 12

        return (
                uncompressed_size.to_bytes(4, 'little') +
                compressed_size.to_bytes(4, 'little') +
                flag_byte.to_bytes(4, 'little') +
                compressed_stream.getvalue()
        )

    @file_reaper
    def run(self):
        DataSet = namedtuple('DataSet',
                             ['data', 'name', 'uncompressed_size'])
        data_set = []
        zip_set = []
        file_list = os.listdir(self.file_name)

        with open(os.path.join(self.output_folder,
                               os.path.basename(self.file_name) + '.pkg'), 'wb') as new_pkg:

            for file in file_list:
                file_path = os.path.join(self.file_name, file)

                with open(file_path, 'rb') as f:
                    d = f.read()
                    data_set.append(DataSet(d, file, len(d)))

            new_pkg.write(b'\0' * 4)
            new_pkg.write(len(data_set).to_bytes(4, 'little'))
            current_offset = 0x50 * len(data_set) + 8
            file_count = len(data_set)

            for key, value in enumerate(data_set):

                print(f'{localize.saving}: {value.name}...')
                self.update_signal.emit(int(100 / file_count * int(key)), f'{key}/{file_count}',
                                        f'{localize.saving} - {value.name}...', False)

                new_pkg.write(value.name.encode('utf-8').ljust(0x40, b'\0'))
                new_pkg.write(value.uncompressed_size.to_bytes(4, 'little'))

                if self.COMPRESSED:

                    for i in range(256):

                        if i.to_bytes(1) not in value.data:
                            zip_byte = i
                            break

                    else:
                        counter = Counter(value.data)
                        zip_byte = counter.most_common()[-1][0]

                zip_data = self.compress_data(value.data, zip_byte) if self.COMPRESSED else value.data
                zip_size = len(zip_data) if self.COMPRESSED else value.uncompressed_size
                zip_set.append(zip_data)
                new_pkg.write(zip_size.to_bytes(4, 'little'))
                new_pkg.write(current_offset.to_bytes(4, 'little'))
                new_pkg.write(self.COMPRESSED.to_bytes(4, 'little'))
                current_offset += zip_size

            for z in zip_set:
                new_pkg.write(z)

        self.update_signal.emit(100, f'{file_count}/{file_count}', localize.done, True)
