import os
import zlib
from collections import namedtuple

from icecream import ic
from source.reaper import Reaper, file_reaper
from source.reapers.idtech.bimage import Bimage2DDS


class Tango(Reaper):
    # For unpacking *.tangoresource from The Evil Within

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as tango:
            magic = tango.read(4)

            if not self.magic([b'\x23\x94\xAB\xCD', ], magic, 'The Evil Within'):
                return

            file_count = int.from_bytes(tango.read(4), 'big')
            FileData = namedtuple('FileData', ['name_index', 'offset', 'zip_size', 'unzip_size'])
            file_data = []

            for _ in range(file_count):
                name_long = int.from_bytes(tango.read(4), 'little')
                file_name = tango.read(name_long).decode('utf-8', errors='ignore')
                name2_long = int.from_bytes(tango.read(4), 'little')
                file_name2 = tango.read(name2_long).decode('utf-8', errors='ignore')
                hash_data = tango.read(4)

            pos0 = tango.tell()
            list_offset = int.from_bytes(tango.read(4), 'big')
            tango.seek(list_offset)
            files_and_folders = int.from_bytes(tango.read(4), 'big')
            tango.seek(8, 1)
            var1 = int.from_bytes(tango.read(4), 'big')
            var2 = int.from_bytes(tango.read(4), 'big')
            pos = (var1 + var2) * 2
            tango.seek(pos, 1)
            ic(file_count, files_and_folders, hex(pos0), hex(list_offset), hex(pos))

            file_list_len = int.from_bytes(tango.read(4), 'big')
            file_count = int.from_bytes(tango.read(4), 'big')
            name_list = [name.decode('utf-8', errors='ignore') for name in tango.read(file_list_len).split(b'\0')]

            for _ in range(files_and_folders):
                name_index = int.from_bytes(tango.read(4), 'big')
                offset = int.from_bytes(tango.read(4), 'big')
                zip_size = int.from_bytes(tango.read(4), 'big')
                unzip_size = int.from_bytes(tango.read(4), 'big')

                file_data.append(FileData(name_index, offset, zip_size, unzip_size))
            
            for j, data in enumerate(file_data):
                name = name_list[data.name_index]
                file_path = f"{self.output_folder}\\{name}"
                ic(name, data.offset, data.zip_size, data.unzip_size)

                tango.seek(data.offset)
                fdata = tango.read(data.zip_size)

                if data.zip_size != data.unzip_size:
                    obj = zlib.decompressobj(-15)
                    fdata = obj.decompress(fdata)

                self.file_save(file_path, fdata)
                
                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if 'bimage' in file_path:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = file_path
                        bimage2dds.output_folder = os.path.dirname(file_path)
                        bimage2dds.run()

                        if self.setting['Main']['save_original_images'] == '1':
                            os.remove(file_path)
                
                self.update_pb(files_and_folders, j + 1, name)


  