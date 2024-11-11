import os
from collections import namedtuple
from source.reaper import Reaper, file_reaper


class AlienIsolation(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as alien:
            magic = alien.read(4)

            if not self.magic([b'PAK2', b'\0' * 4], magic, 'Alien: Isolation'):
                return

            if magic == b'PAK2':
                names_len = int.from_bytes(alien.read(4), byteorder="little")
                file_count = int.from_bytes(alien.read(4), byteorder="little")
                alien.seek(0x10)
                file_names = [n.decode('utf-8', errors='ignore') for n in alien.read(names_len).split(b'\0')]

                for i in range(file_count):
                    name = file_names[i]
                    offset = int.from_bytes(alien.read(4), byteorder="little")
                    size = int.from_bytes(alien.read(4), byteorder="little") - offset

                    path = os.path.join(self.output_folder, name)
                    os.makedirs(os.path.dirname(path), exist_ok=True)

                    with open(path, 'wb') as new_file:
                        here = alien.tell() - 4
                        alien.seek(offset)
                        new_file.write(alien.read(size))
                        alien.seek(here)

                    self.update_pb(file_count, i + 1, name)

            elif magic == b'\0' * 4:
                name_data = os.path.basename(self.file_name).split('.')
                folder_data = os.path.dirname(self.file_name)
                bin_file_path = name_data[0] + '_HEADERS.ALL.BIN'

                with open(os.path.join(folder_data, bin_file_path), 'rb') as bin_file:
                    bin_file.seek(4)
                    files_count = int.from_bytes(bin_file.read(4), byteorder="little")
                    names_len = int.from_bytes(bin_file.read(4), byteorder="little")
                    file_names = [n.decode('utf-8', errors='ignore') for n in bin_file.read(names_len - 16).split(b'\0')]
                    # print(len(file_names), files_count)

                    bin_file.seek(names_len)
                    FileData = namedtuple('FileData',
                                          ['size', 'offset', 'name'])
                    file_data = []

                    for i in range(files_count):
                        header = bin_file.read(4)
                        unk1 = int.from_bytes(bin_file.read(4), byteorder="little")
                        zeros = int.from_bytes(bin_file.read(4), byteorder="little")
                        file_size = int.from_bytes(bin_file.read(4), byteorder="little")
                        file_offset = int.from_bytes(bin_file.read(4), byteorder="little")

                        file_data.append(FileData(file_size, file_offset, file_names[i]))

                    start = alien.tell()

                    for j, file in enumerate(file_data):
                        alien.seek(file.offset + start)
                        d = alien.read(file.size)
                        full_name = os.path.join(self.output_folder, file.name)
                        os.makedirs(os.path.dirname(full_name), exist_ok=True)

                        with open(full_name, 'wb') as nf:
                            nf.write(d)

                        self.update_pb(files_count, j + 1, file.name)
