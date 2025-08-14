import os
from collections import namedtuple
from icecream import ic

from source.reaper import Reaper, file_reaper
from source.reapers.idtech.bimage import Bimage2DDS
from source.codecs.zip_methods import ZipMethods


class Resources(Reaper):

    def __init__(self, game_name, res_path, index_path, res_header, index_header, fco, step_sz, zip_alg, offset_bites,
                 engine=5):
        super().__init__()
        self.game_name = game_name
        self.resource_path = res_path
        self.index_path = index_path
        self.resource_header = res_header
        self.index_header = index_header
        self.file_count_offset = fco
        self.step_size = step_sz
        self.offset_bites = offset_bites
        self.zip_algo = zip_alg
        self.engine = engine

    @file_reaper
    def run(self):

        FileList = namedtuple('FileList',
                              ['index', 'dest_name', 'offset', 'unzip_size', 'zip_size'])
        file_list = []

        with open(self.index_path, 'rb') as index_file:

            if not self.magic([self.index_header, ], index_file.read(4), self.game_name):
                self.update_pb(0, 0, '')
                return

            index_file.seek(self.file_count_offset)
            file_count = int.from_bytes(index_file.read(4), byteorder='big')

            for i in range(file_count):
                index = int.from_bytes(index_file.read(4), byteorder='big')
                type_len = int.from_bytes(index_file.read(4), byteorder='little')
                file_type = index_file.read(type_len).decode('utf-8')
                name_len = int.from_bytes(index_file.read(4), byteorder='little')
                source_file = index_file.read(name_len).decode('utf-8')
                dest_name_len = int.from_bytes(index_file.read(4), byteorder='little')
                ic(file_type)

                if dest_name_len:
                    dest_name = index_file.read(dest_name_len).decode('utf-8')
                else:
                    dest_name = source_file

                offset = int.from_bytes(index_file.read(self.offset_bites), byteorder='big')
                unzip_size = int.from_bytes(index_file.read(4), byteorder='big')
                zip_size = int.from_bytes(index_file.read(4), byteorder='big')

                step_size = int.from_bytes(index_file.read(4), byteorder='big')
                index_file.seek(((24 * step_size) + self.step_size) if self.engine == 5 else self.step_size, 1)

                file_list.append(FileList(index, dest_name, offset, unzip_size, zip_size))

        with open(self.resource_path, 'rb') as res_file:

            if not self.magic([self.resource_header, ], res_file.read(4), self.game_name):
                return

            for i, f in enumerate(file_list):

                if f.dest_name:
                    res_file.seek(f.offset)
                    path = f"{self.output_folder}\\{f.dest_name}"

                    if f.zip_size or f.unzip_size:
                        self.file_save(path, res_file.read(f.zip_size))

                        if f.zip_size != f.unzip_size and self.zip_algo is not None:
                            self.unzip(path, self.zip_algo)

                        if self.setting['Main']['save_original_images'] in ['1', '2'] and 'bimage' in path:
                            bimage2dds = Bimage2DDS()
                            bimage2dds.file_name = path
                            bimage2dds.output_folder = os.path.dirname(path)
                            bimage2dds.run()

                            if self.setting['Main']['save_original_images'] == '1':
                                os.remove(path)

                    self.update_pb(file_count, i + 1, f.dest_name)


class Dishonored(Reaper):
    # For unpacking *.resource, *.index from Dishonored 2 and Dishonored: Death of the Outsider

    def run(self):
        ext = self.file_name.split('.')[-1]
        game_name = '"Dishonored" 2 or "Dishonored: Death of the Outsider"'
        resource_path = self.file_name.replace(ext, 'resources')
        index_path = self.file_name.replace(ext, 'index')
        resource_header = b'\x04SER'
        index_header = b'\x05SER'
        file_count_offset = 0x20
        step_size = 6
        offset_bites = 8
        # zip_algo = ZipMethods.DEFLATE_NOERROR
        zip_algo = None

        res = Resources(game_name, resource_path, index_path, resource_header, index_header,
                        file_count_offset, step_size, zip_algo, offset_bites)
        res.file_name = self.file_name
        res.output_folder = self.output_folder
        res.update_pb = self.update_pb
        res.run()


class Wolfenstein(Reaper):
    # For unpacking *.resource, *.index from Wolfenstein: The Old Blood and Wolfenstein: The New Order

    def run(self):
        ext = self.file_name.split('.')[-1]
        game_name = 'Wolfenstein: The Old Blood or Wolfenstein: The New Order'
        resource_path = self.file_name.replace(ext, 'resources')
        index_path = self.file_name.replace(ext, 'index')
        resource_header = b'\x03SER'
        index_header = b'\x03SER'
        file_count_offset = 0x24
        step_size = 5
        offset_bites = 4
        zip_algo = ZipMethods.DEFLATE_NOERROR

        res = Resources(game_name, resource_path, index_path, resource_header, index_header,
                        file_count_offset, step_size, zip_algo, offset_bites)
        res.file_name = self.file_name
        res.output_folder = self.output_folder
        res.update_pb = self.update_pb
        res.run()

class Rage(Reaper):
    # For unpacking *.resource from Rage

    def run(self):

        with open(self.file_name, 'rb') as rf:
            rf.seek(4)
            file_count_offset = int.from_bytes(rf.read(4), byteorder='big')

        game_name = 'Rage'
        resource_path = self.file_name
        index_path = self.file_name
        resource_header = b'\x22\x94\xAB\xCD'
        index_header = b'\x22\x94\xAB\xCD'
        step_size = 0x14
        offset_bites = 4
        zip_algo = ZipMethods.DEFLATE_NOERROR

        res = Resources(game_name, resource_path, index_path, resource_header, index_header,
                        file_count_offset, step_size, zip_algo, offset_bites)
        res.file_name = self.file_name
        res.output_folder = self.output_folder
        res.update_pb = self.update_pb
        res.run()

class Doom2016(Reaper):
    # For unpacking *.resource, *.index, *.pindex, *.patch from Doom (2016)

    def run(self):
        ext = self.file_name.split('.')[-1]

        if ext in ('index', 'pindex'):
            ext2 = 'patch' if os.path.exists(self.file_name.replace(ext, 'patch')) else 'resources'
            resource_path = self.file_name.replace(ext, ext2)
            index_path = self.file_name
        else:
            ext2 = 'index' if os.path.exists(self.file_name.replace(ext, 'index')) else 'pindex'
            resource_path = self.file_name
            index_path = self.file_name.replace(ext, ext2)

        game_name = 'Doom (2016)'
        resource_header = b'\x05SER'
        index_header = b'\x05SER'
        file_count_offset = 0x20
        step_size = 1
        offset_bites = 8
        zip_algo = ZipMethods.DEFLATE_NOERROR

        res = Resources(game_name, resource_path, index_path, resource_header, index_header,
                        file_count_offset, step_size, zip_algo, offset_bites, engine=6)
        res.file_name = self.file_name
        res.output_folder = self.output_folder
        res.update_pb = self.update_pb
        res.run()
