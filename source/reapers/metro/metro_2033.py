
import os
import io
from  collections import namedtuple
from source.reaper import Reaper, file_reaper

FileData = namedtuple('FileData',
                       ['offset', 'zip_size', 'unzip_size', 'file_name', 'hash_sum'])
file_list = {}

class Metro(Reaper):

    get_ext = {
        'content': 'dat',
        'sounds': 'ogg',
        'textures': 'tex',
        'videos': 'ogv'
    }
        

    @file_reaper
    def run(self):
        file_size = os.path.getsize(self.file_name)
        path_to_files = os.path.dirname(self.file_name)

        if 'content.vfi' not in self.file_name:
            file_name = os.path.basename(self.file_name)
            self.file_name = self.file_name.replace(file_name, 'content.vfi')
            file_size = os.path.getsize(self.file_name)

            if not os.path.exists(self.file_name):
                self.magic([b'\xFF' * 4], b'\0', 'Metro 2033 VFI')
                return

        with open(self.file_name, "rb") as vfi_file:
            magic = vfi_file.read(4)

            if not self.magic([b'\xFF' * 4], magic, 'Metro 2033 VFI'):
                return

            vfi_file.seek(0x28)

            while vfi_file.tell() < file_size:
                archive_name_len = int.from_bytes(vfi_file.read(4), 'little') - 4
                archive_name = (vfi_file.read(archive_name_len)
                                        .decode('utf-8', errors='ignore')
                                        .strip('\0'))
                archive_size = int.from_bytes(vfi_file.read(4), 'little')
                one = int.from_bytes(vfi_file.read(4), 'little') # Always 1
                data_size = int.from_bytes(vfi_file.read(4), 'little') - 4
                vfi_file.seek(4, 1)
                archive_data = io.BytesIO( vfi_file.read(data_size))
                temp_list = []

                while archive_data.tell() < data_size:
                    offset = int.from_bytes(archive_data.read(4), 'little')
                    zip_size = int.from_bytes(archive_data.read(4), 'little')
                    unzip_size = int.from_bytes(archive_data.read(4), 'little')
                    file_name_size = int.from_bytes(archive_data.read(4), 'little')
                    file_name = str(int.from_bytes(archive_data.read(file_name_size), 'little'))[:20]
                    hash_sum = archive_data.read(4)

                    temp_list.append(FileData(offset, zip_size, unzip_size, file_name, hash_sum))

                file_list[archive_name] = temp_list
                vfi_file.seek(0x18, 1)

            file_count = 0
            current_file = 0

            for f in file_list.keys():
                file_count += len(file_list[f])

            for name in file_list.keys():

                with open(f'{path_to_files}\\{name}', 'rb') as vol:
                    only_name = name.split('.')[0]
                    second_part = name.split('.')[1]

                    for file in file_list[name]:
                        current_file += 1
                        vol.seek(file.offset)
                        data = vol.read(file.zip_size)
                        path = f'{self.output_folder}\\{only_name}\\{second_part}\\{file.file_name}.{self.get_ext.get(only_name, 'dat')}'
                        self.file_save(path, data)
                        self.update_pb(file_count, current_file, file.file_name)

