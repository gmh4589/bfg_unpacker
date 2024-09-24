import os
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

            for i in range(file_count):
                name_long = int.from_bytes(tango.read(4), 'little')
                file_name = tango.read(name_long).decode('utf-8', errors='ignore')
                name2_long = int.from_bytes(tango.read(4), 'little')
                file_name2 = tango.read(name2_long).decode('utf-8', errors='ignore')
                hash_data = tango.read(4)

            list_offset = int.from_bytes(tango.read(4), 'big')
            tango.seek(list_offset + 12)
            file_count = int.from_bytes(tango.read(4), 'big')
            wtf = int.from_bytes(tango.read(4), 'big')
            tango.seek((file_count + wtf) * 2 + tango.tell())
            file_list_len = int.from_bytes(tango.read(4), 'big')
            file_count = int.from_bytes(tango.read(4), 'big')
            name_list = [name.decode('utf-8', errors='ignore') for name in tango.read(file_list_len).split(b'\0')]

            for j in range(file_count):
                name_index = int.from_bytes(tango.read(4), 'big')
                name = name_list[name_index].split(':')[-1]
                path = os.path.join(self.output_folder, name)
                offset = int.from_bytes(tango.read(4), 'big')
                zip_size = int.from_bytes(tango.read(4), 'big')
                unzip_size = int.from_bytes(tango.read(4), 'big')
                here = tango.tell()
                tango.seek(offset)
                zip_data = tango.read(zip_size)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as nf:
                    nf.write(zip_data)

                if zip_size != unzip_size:
                    self.unzip(path, 171)

                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if 'bimage' in path:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = path
                        bimage2dds.output_folder = os.path.dirname(path)
                        bimage2dds.run()

                if self.setting['Main']['save_original_images'] == '1':
                    os.remove(path)

                tango.seek(here)
                self.update_pb(file_count, j + 1, name)

            print(tango.tell())
