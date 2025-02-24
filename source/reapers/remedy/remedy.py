
import os

from source.reaper import Reaper, file_reaper
from collections import namedtuple

from source.ui import localize


class Remedy(Reaper):

    @file_reaper
    def run(self):
        NameData = namedtuple("NameData",
                              ['name', 'offset', 'size'])
        name_data = []
        files = []

        only_name = self.file_name.split('.')[0]
        bin_file = f'{only_name}.bin'
        rmdp_file = f'{only_name}.rmdp'
        bin_size = os.path.getsize(bin_file)

        if not os.path.exists(bin_file) or not os.path.exists(rmdp_file):
            print(localize.not_correct_file.replace('%%', 'NorthLight Engine'))
            self.update_signal.emit(100, '', localize.not_correct_file.replace('%%', 'NorthLight Engine'), True)
            return

        with open(bin_file, 'rb') as bin_data:
            byteorder_id = bin_data.read(1)

            if byteorder_id == b'\x01':
                byteorder = "big"
            else:
                byteorder = "little"

            ver = int.from_bytes(bin_data.read(4), byteorder=byteorder)

            match ver:
                # TODO: Alan Wake Remastered, Alan Wake 2
                case 2:
                    print('Alan Wake')
                case 7:
                    print('Alan Wakes American Nightmare')
                case 8:
                    print('Quantum Break')
                case 9:
                    print('Control')

            folders_count = int.from_bytes(bin_data.read(4), byteorder=byteorder)
            files_count = int.from_bytes(bin_data.read(4), byteorder=byteorder)
            bin_data.seek(8 if ver > 2 else 0, 1)
            name_size = int.from_bytes(bin_data.read(4), byteorder=byteorder)
            ver = 10 if 'remastered' in self.file_name.lower() else ver

            if ver == 10:
                file_data_start = bin_size - name_size - (0x40 * files_count) + 8
            else:
                bin_data.seek(0x80 + folders_count * (48 if ver >= 8 else 28), 1)
                file_data_start = bin_data.tell()

            bin_data.seek(bin_size - name_size)
            files_raw = [file.decode('utf-8', errors='ignore') for file in bin_data.read(name_size).split(b'\0')]

            folder = True
            folder_names = []
            folder_names_old = []

            for file in files_raw:

                if '.' in file:
                    folder = False

                    if len(folder_names) <= len(folder_names_old):
                        folder_names = folder_names_old[:-len(folder_names)] + folder_names

                    files.append('\\'.join(folder_names) + '\\' + file)

                elif ':' in file:
                    pass

                else:

                    if folder_names and not folder:
                        folder_names_old = folder_names
                        folder_names = [file]
                        folder = True
                    else:
                        folder_names.append(file)

            bin_data.seek(file_data_start)

            for i in range(files_count):
                here = hex(bin_data.tell())
                bin_data.seek(32 if ver >= 8 else 20, 1)
                offset = int.from_bytes(bin_data.read(8), byteorder=byteorder)
                size = int.from_bytes(bin_data.read(8), byteorder=byteorder)

                full_name = f"{self.output_folder}\\{files[i]}"
                name_data.append(NameData(full_name, offset, size))

                # bin_data.seek(12 if ver >= 7 else (16 if ver == 10 else 4), 1)
                bin_data.seek(12 if ver in (7, 8, 9) else (16 if ver == 10 else 4), 1)

        with open(rmdp_file, 'rb') as rmdp_data:

            for i, data_file in enumerate(name_data):
                rmdp_data.seek(data_file.offset)
                data = rmdp_data.read(data_file.size)
                os.makedirs(os.path.dirname(data_file.name), exist_ok=True)

                with open(data_file.name, "wb") as nf:
                    nf.write(data)

                self.update_pb(files_count, i + 1, data_file.name)
