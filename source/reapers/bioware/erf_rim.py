import io
from collections import namedtuple

from icecream import ic

from source.reaper import Reaper, file_reaper
from source.reapers.bioware.ext import get_ext
from source.codecs.zip_methods import ZipMethods
from source.ui import localize


class ERFUnpacker(Reaper):

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as f:
            magic = f.read(4)

            if not self.magic([b'RIM ', b'ERF ', b'HAK ', b'MOD ', b'E\x00R\x00', b'R\x00I\x00'], magic, 'BioWare Engines'):
                return

            if magic in (b'RIM ', b'ERF ', b'HAK ', b'MOD '):
                ver = f.read(4).decode('utf-8', errors='ignore')
            else:
                f.seek(8)
                ver = f.read(8).decode('utf-16', errors='ignore')

            ic(ver)
            FileData = namedtuple('FileData',
                        ['name', 'offset', 'zip_size', 'unzip_size'])
            file_data = []

            if ver == 'V1.0':  # Version 1
                f.seek(0x10) if magic in (b'ERF ', b'MOD ') else f.seek(0xC)
                file_count = int.from_bytes(f.read(4), byteorder='little')
                off_list = int.from_bytes(f.read(4), byteorder='little')

                file_name_array = []

                f.seek(off_list)

                for _ in range(file_count):
                    file_name = f.read(0x10).rstrip(b'\x00').decode('utf-8', errors='ignore')
                    index = int.from_bytes(f.read(4), byteorder='little') if magic in (b'ERF ', b'MOD ') else None
                    ext = get_ext.get(int.from_bytes(f.read(4), byteorder='little'), 'dat')
                    file_name_array.append(f'{file_name}.{ext}')

                    if magic == b'RIM ':
                        index = int.from_bytes(f.read(4), byteorder='little')
                        offset = int.from_bytes(f.read(4), byteorder='little')
                        file_size = int.from_bytes(f.read(4), byteorder='little')
                        file_data.append(FileData(f'{file_name}.{ext}', offset, file_size, file_size))

                if magic in (b'ERF ', b'MOD '):

                    for j in range(file_count):
                        offset = int.from_bytes(f.read(4), byteorder='little')
                        file_size = int.from_bytes(f.read(4), byteorder='little')
                        file_name = file_name_array[j]
                        file_data.append(FileData(file_name, offset, file_size, file_size))

            elif ver == 'V1.1':  # Version 1.1
                f.seek(0x10) 
                file_count = int.from_bytes(f.read(4), byteorder='little')
                off_list = int.from_bytes(f.read(4), byteorder='little')

                file_name_array = []

                f.seek(off_list)

                for _ in range(file_count):
                    file_name = f.read(0x20).rstrip(b'\x00').decode('utf-8', errors='ignore')
                    index = int.from_bytes(f.read(4), byteorder='little') 
                    ext = get_ext.get(int.from_bytes(f.read(4), byteorder='little'), 'dat')
                    file_name_array.append(f'{file_name}.{ext}')

                for i in range(file_count):
                    offset = int.from_bytes(f.read(4), byteorder='little')
                    file_size = int.from_bytes(f.read(4), byteorder='little')
                    file_data.append(FileData(file_name_array[i], offset, file_size, file_size))
            
            elif ver == 'V2.0':  # Version 2
                f.seek(0x10, 0)
                file_count = int.from_bytes(f.read(4), byteorder='little')
                f.seek(0x20, 0)

                for i in range(file_count):
                    name = f.read(0x40).decode('utf-16', errors='ignore').strip('\0')
                    offset = int.from_bytes(f.read(4), byteorder='little')
                    size = int.from_bytes(f.read(4), byteorder='little')
                    file_data.append(FileData(name, offset, size, size))

            elif ver == 'V3.0':  # Version 3
                # TODO: File extracted without compressions. I don't know what is an algorythm used here (Dragon Age II)
                
                f.seek(0x10)
                names_long = int.from_bytes(f.read(4), byteorder='little')
                file_count = int.from_bytes(f.read(4), byteorder='little')
                f.seek(0x30)
                names = f.read(names_long)

                for i in range(file_count):
                    index = int.from_bytes(f.read(4), byteorder='little')
                    hash_sum = int.from_bytes(f.read(0xC), byteorder='little')
                    offset = int.from_bytes(f.read(4), byteorder='little')
                    zip_size = int.from_bytes(f.read(4), byteorder='little')
                    size = int.from_bytes(f.read(4), byteorder='little')

                    if index != 0xFFFFFFFF:
                        name = self.get_name(io.BytesIO(names[index:]))
                    else:
                        name = f'{i:08}.dat'

                    file_data.append(FileData(name, offset, zip_size, size))

            else:
                print(localize.not_correct_file.replace('%%', 'BioWare Engines'))
                self.update_pb(1, 1, localize.not_correct_file.replace('%%', 'BioWare Engines'))
                return

            for i, file in enumerate(file_data):
                f.seek(file.offset)
                data = f.read(file.unzip_size)
            
                self.file_save(f"{self.output_folder}\\{file.name}", data)
                self.update_pb(file_count, i + 1, file.name)
