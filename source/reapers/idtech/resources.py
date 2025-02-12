import os
from source.reaper import Reaper, file_reaper
from source.reapers.idtech.bimage import Bimage2DDS
from source.codecs.zip_methods import ZipMethods


# TODO: Very slow unpacking... 🐌
class Resources(Reaper):
    # For unpack *.index, *.pindex, *.resources, *.patch files from Doom (2016)
    # For unpack *.resources and *.patch files from Rage

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

        mode = 'doom2016' if os.path.exists(index_path) else 'rage'
        reso_file = open(resource_path, 'rb')

        if mode == 'doom2016':
            index_file = open(index_path, 'rb')
            magic = index_file.read(4)
            list_file = index_file

            if not self.magic([b'\x05SER', ], magic, 'Doom (2016)'):
                return

        # For Rage
        else:
            list_file = reso_file
            list_file.seek(4)

        file_list_long = int.from_bytes(list_file.read(4), byteorder='big')
        list_file.seek(0x20 if mode == 'doom2016' else file_list_long)
        file_count = int.from_bytes(list_file.read(4), byteorder='big')

        for i in range(file_count):
            index = int.from_bytes(list_file.read(4), byteorder='big')
            type_len = int.from_bytes(list_file.read(4), byteorder='little')
            file_type = list_file.read(type_len).decode('utf-8')
            name_len = int.from_bytes(list_file.read(4), byteorder='little')
            source_file = list_file.read(name_len).decode('utf-8')
            dest_name_len = int.from_bytes(list_file.read(4), byteorder='little')

            if dest_name_len:
                dest_file = list_file.read(dest_name_len).decode('utf-8')
            else:
                dest_file = source_file

            offset = int.from_bytes(list_file.read(8 if mode == 'doom2016' else 4), byteorder='big')
            unzip_size = int.from_bytes(list_file.read(4), byteorder='big')
            zip_size = int.from_bytes(list_file.read(4), byteorder='big')

            if mode == 'rage':
                skip = int.from_bytes(reso_file.read(4), byteorder='big')
                reso_file.seek((0x18 * skip) + 0x14, 1)
            else:
                list_file.seek(5, 1)

            here = reso_file.tell()

            if zip_size:
                reso_file.seek(offset)
                zip_data = reso_file.read(zip_size)
                path = os.path.join(self.output_folder, dest_file)
                os.makedirs(os.path.dirname(path), exist_ok=True)

                with open(path, 'wb') as nf:
                    nf.write(zip_data)

                if zip_size != unzip_size:
                    self.unzip(path, ZipMethods.DEFLATE_NOERROR)

                if self.setting['Main']['save_original_images'] in ['1', '2']:

                    if 'bimage' in path:
                        bimage2dds = Bimage2DDS()
                        bimage2dds.file_name = path
                        bimage2dds.output_folder = os.path.dirname(path)
                        bimage2dds.run()

                if self.setting['Main']['save_original_images'] == '1':
                    os.remove(path)

                reso_file.seek(here)

            self.update_pb(file_count, i + 1, dest_file)

        if mode == 'doom2016':
            index_file.close()

        resource_path.close()
