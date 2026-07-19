import os
from collections import namedtuple
import zlib

from source.reaper import Reaper, file_reaper
from source.reapers.idtech.bimage import Bimage2DDS
from source.ui import localize


class Patch(Reaper):

    @file_reaper
    def run(self):
        ext = self.file_name.split('.')[-1]
        
        resource_path = self.file_name.replace(ext, 'resources')
        index_path = self.file_name.replace(ext, 'index')
        patch_path = self.file_name.replace(ext, 'patch')
        pindex_path = self.file_name.replace(ext, 'pindex')

        FileList = namedtuple('FileList',
                              ['index', 'dest_name', 'offset', 'unzip_size', 'zip_size'])

        if not os.path.exists(index_path) \
            or not os.path.exists(pindex_path) \
                or not os.path.exists(patch_path) \
                    or not os.path.exists(resource_path):
            print(f"{localize.not_correct_file} {self.file_name} DOOM (2016)!")
            return
        
        def get_fl(path):

            with open(path, 'rb') as index_file:
                file_list = []

                if not self.magic([b'\x05SER', ], index_file.read(4), 'DOOM (2016)'):
                    self.update_pb(0, 0, '')
                    return

                index_file.seek(0x20)
                file_count = int.from_bytes(index_file.read(4), byteorder='big')

                for i in range(file_count):
                    index = int.from_bytes(index_file.read(4), byteorder='big')
                    type_len = int.from_bytes(index_file.read(4), byteorder='little')
                    file_type = index_file.read(type_len).decode('utf-8')
                    name_len = int.from_bytes(index_file.read(4), byteorder='little')
                    source_file = index_file.read(name_len).decode('utf-8')
                    dest_name_len = int.from_bytes(index_file.read(4), byteorder='little')

                    if dest_name_len:
                        dest_name = index_file.read(dest_name_len).decode('utf-8')
                    else:
                        dest_name = source_file

                    offset = int.from_bytes(index_file.read(8), byteorder='big')
                    unzip_size = int.from_bytes(index_file.read(4), byteorder='big')
                    zip_size = int.from_bytes(index_file.read(4), byteorder='big')
                    index_file.seek(5, 1)

                    file_list.append(FileList(index, dest_name, offset, unzip_size, zip_size))

            return file_list, file_count

        file_list, file_count = get_fl(index_path)
        p_file_list, _ = get_fl(pindex_path)
        
        res_file = open(resource_path, 'rb') 
        pacth_file = open(patch_path, 'rb') 

        if not self.magic([b'\x05SER', ], res_file.read(4), 'DOOM (2016)'):
            res_file.close()
            pacth_file.close()
            return
        
        if not self.magic([b'\x05SER', ], pacth_file.read(4), 'DOOM (2016)'):
            res_file.close()
            pacth_file.close()
            return

        for i, f in enumerate(file_list):

            if f.dest_name:

                if f == p_file_list[i]:
                    file = res_file
                else:
                    file = pacth_file
                    f = p_file_list[i]

                file.seek(f.offset)
                path = f"{self.output_folder}\\{f.dest_name}"

                if f.zip_size or f.unzip_size:
                    data = file.read(f.zip_size)

                    if f.zip_size != f.unzip_size and data:
                        try:
                            obj = zlib.decompressobj(-15)
                            data = obj.decompress(data)
                        except zlib.error:
                            data = self.smart_deflate(data)

                    self.file_save(path, data)

                    if self.setting['Main']['save_original_images'] in ['1', '2'] and 'bimage' in path:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = path
                        bimage2dds.output_folder = os.path.dirname(path)
                        bimage2dds.run()

                        if self.setting['Main']['save_original_images'] == '1':
                            os.remove(path)

                self.update_pb(file_count, i + 1, f.dest_name)
        
        res_file.close()
        pacth_file.close()
