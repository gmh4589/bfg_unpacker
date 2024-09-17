
import os
from icecream import ic
from source.reaper import Reaper, file_reaper
from source.ui import localize


class Doom2016(Reaper):
    # For unpack *.index, *.pindex, *.resources, *.patch files from Doom (2016)

    @file_reaper
    def run(self):
        ext = self.file_name.split('.')[-1]

        if ext in ('index', 'pindex'):
            ext2 = 'patch' if ext == 'pindex' else 'resources'
            resource_path = self.file_name.replace(ext, ext2)
            index_path = self.file_name
        elif ext in ('patch', 'resources'):
            ext2 = 'index' if ext == 'resources' else 'pindex'
            resource_path = self.file_name
            index_path = self.file_name.replace(ext, ext2)
        else:
            print(localize.not_correct_file.replace('%%', 'Doom (2016) file'))
            self.update_signal.emit(100, '', '', True)
            return

        if not os.path.exists(resource_path) or not os.path.exists(index_path):
            self.update_signal.emit(100, '', '', True)
            return

        ic(resource_path, index_path)

        with open(index_path, 'rb') as index_file:
            magic = index_file.read(4)

            if magic != b'\x05SER':
                print(localize.not_correct_file.replace('%%', 'Doom (2016) file'))
                self.update_signal.emit(100, '', '', True)
                return

            with open(resource_path, 'rb') as patch_file:
                file_list_long = int.from_bytes(index_file.read(4), byteorder='big')
                index_file.seek(0x20)
                file_count = int.from_bytes(index_file.read(4), byteorder='big')

                for i in range(file_count):
                    index = int.from_bytes(index_file.read(4), byteorder='big')
                    type_len = int.from_bytes(index_file.read(4), byteorder='little')
                    file_type = index_file.read(type_len).decode('utf-8')
                    name_len = int.from_bytes(index_file.read(4), byteorder='little')
                    source_file = index_file.read(name_len).decode('utf-8')
                    dist_len = int.from_bytes(index_file.read(4), byteorder='little')

                    if dist_len == 0:
                        dest_file = source_file
                    else:
                        dest_file = index_file.read(dist_len).decode('utf-8')

                    offset = int.from_bytes(index_file.read(8), byteorder='big')
                    unzip_size = int.from_bytes(index_file.read(4), byteorder='big')
                    zip_size = int.from_bytes(index_file.read(4), byteorder='big')
                    index_file.seek(5, 1)

                    if zip_size:
                        patch_file.seek(offset)
                        zip_data = patch_file.read(zip_size)
                        path = os.path.join(self.output_folder, dest_file)
                        os.makedirs(os.path.dirname(path), exist_ok=True)

                        with open(path, 'wb') as nf:
                            nf.write(zip_data)

                        self.unzip(path, 171)

                    self.update_pb(file_count, i + 1, dest_file)


class RageResources(Reaper):
    # For unpack *.resources and *.patch files from Rage

    @file_reaper
    def run(self):

        with open(self.file_name, 'rb') as reso_file:
            magic = reso_file.read(4)

            if magic != b'\x22\x94\xAB\xCD':
                print(localize.not_correct_file.replace('%%', 'Rage gameresources.resources file'))
                self.update_signal.emit(100, '', '', True)
                return

            start_offset = int.from_bytes(reso_file.read(4), byteorder='big')
            reso_file.seek(start_offset)
            file_count = int.from_bytes(reso_file.read(4), byteorder='big')

            for i in range(file_count):
                index = int.from_bytes(reso_file.read(4), byteorder='big')
                type_long = int.from_bytes(reso_file.read(4), byteorder='little')
                type_name = reso_file.read(type_long).decode('utf-8')
                source_name_len = int.from_bytes(reso_file.read(4), byteorder='little')
                source_name = reso_file.read(source_name_len).decode('utf-8')
                dest_name_len = int.from_bytes(reso_file.read(4), byteorder='little')

                if dest_name_len:
                    dest_name = reso_file.read(dest_name_len).decode('utf-8')
                else:
                    dest_name = source_name

                offset = int.from_bytes(reso_file.read(4), byteorder='big')
                unzip_size = int.from_bytes(reso_file.read(4), byteorder='big')
                zip_size = int.from_bytes(reso_file.read(4), byteorder='big')
                skip = int.from_bytes(reso_file.read(4), byteorder='big')
                reso_file.seek((0x18 * skip) + 0x14, 1)

                here = reso_file.tell()

                if zip_size:
                    reso_file.seek(offset)
                    path = os.path.join(self.output_folder, dest_name)
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    zip_data = reso_file.read(zip_size)

                    with open(path, 'wb') as zf:
                        zf.write(zip_data)

                    if zip_data != unzip_size:
                        self.unzip(path, 171)

                    reso_file.seek(here)

                self.update_pb(file_count, i + 1, dest_name)


class Bimage2DDS(Reaper):

    @file_reaper
    def run(self):
        pass


class IDWAV2WAV(Reaper):

    @file_reaper
    def run(self):
        pass
