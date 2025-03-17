import os
import zlib
import lz4.frame

from icecream import ic
from collections import namedtuple

from source.reaper import Reaper, file_reaper
from source.ui import localize
from source.ui.custom_ui import CustomDialog
from source.codecs.zip_methods import ZipMethods


class BethesdaArchive(Reaper):
    #  TODO:
    #   retry OBJ files,
    #   add x_mem support
    #   retry Skyrim VR and Fallout 4 VR

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as bsa_file:
            magic = bsa_file.read(4)

            if not self.magic([b'BSA\0', ], magic,'Bethesda Softworks Archive'):
                return

            version = int.from_bytes(bsa_file.read(4), byteorder="little")
            step = 4 if version == 105 else 0
            folder_list_start = int.from_bytes(bsa_file.read(4), byteorder="little")
            flags = int.from_bytes(bsa_file.read(4), byteorder="little")
            directory_names = bool(flags & 0x1)
            file_names = bool(flags & 0x2)
            compressed = bool(flags & 0x4)
            retain_directory = bool(flags & 0x8)
            retain_names = bool(flags & 0x10)
            retain_offsets = bool(flags & 0x20)
            xbox = bool(flags & 0x40)
            startup_strings = bool(flags & 0x80)
            embed_names = bool(flags & 0x100)
            x_mem = bool(flags & 0x200)

            byteorder = 'big' if xbox else 'little'

            folder_count = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
            file_count = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
            all_folders_len = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
            all_files_len = int.from_bytes(bsa_file.read(4), byteorder=byteorder)

            ic(compressed, folder_count, file_count, all_folders_len, all_files_len)
            file_type_flags = int.from_bytes(bsa_file.read(4), byteorder=byteorder)

            nif = bool(file_type_flags & 0x1)
            dds = bool(file_type_flags & 0x2)
            xml = bool(file_type_flags & 0x4)
            wav = bool(file_type_flags & 0x8)
            mp3 = bool(file_type_flags & 0x10)
            txt = bool(file_type_flags & 0x20)
            spt = bool(file_type_flags & 0x40)
            fnt = bool(file_type_flags & 0x80)
            misc = bool(file_type_flags & 0x100)
            x_mem = bool(file_type_flags & 0x200)

            FolderData = namedtuple('FolderData',
                                    ['name_hash', 'files_in_folder', 'offset_to_files'])
            folder_data = []

            self.update_signal.emit(0, '', f'{localize.wait}...', False)

            for i in range(folder_count):
                name_hash = bsa_file.read(8)
                files_in_folder = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                bsa_file.seek(step, 1)
                offset_to_files = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                bsa_file.seek(step, 1)
                folder_data.append(FolderData(name_hash, files_in_folder, offset_to_files))

            FileData = namedtuple('FileData',
                                  ['folder_name', 'name_hash', 'file_size', 'file_info', 'file_offset'])
            file_data = []

            for data in folder_data:

                folder_name_len = int.from_bytes(bsa_file.read(1), byteorder=byteorder)
                folder_name = bsa_file.read(folder_name_len).rstrip(b'\x00').decode('utf-8', errors='ignore')
                # os.makedirs(os.path.join(self.output_folder, folder_name), exist_ok=True)

                for j in range(data.files_in_folder):

                    file_data.append(FileData(
                        folder_name=folder_name,
                        name_hash=bsa_file.read(8),
                        file_size=int.from_bytes(bsa_file.read(3), byteorder=byteorder),
                        file_info=int.from_bytes(bsa_file.read(1)),
                        file_offset=int.from_bytes(bsa_file.read(4), byteorder=byteorder))
                    )

            files_list = [file_name.decode('utf-8', errors='ignore')
                          for file_name in bsa_file.read(all_files_len).split(b'\0') if file_name]

            for k, file_name in enumerate(files_list):

                path = os.path.join(self.output_folder, file_data[k].folder_name, file_name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                bsa_file.seek(file_data[k].file_offset + 4)
                error = False
                ext = file_name.split('.')[-1]
                self.update_pb(file_count, k, file_name)

                if version == 103:

                    if b'\x78\x9C' in bsa_file.read(8):
                        compressed = True

                    if ext in ('mp3', 'ogg', 'png'):
                        compressed = False

                bsa_file.seek(file_data[k].file_offset)

                if compressed:

                    if version in (103, 104):  # 103 - Oblivion, Nehrim, 104 - Skyrim LE, Fallout 3, Fallout NV, Enderal
                        codec = ZipMethods.ZLIB_NOERROR
                        here = bsa_file.tell()

                        if embed_names:
                            name_l = int.from_bytes(bsa_file.read(1))
                            file_name = bsa_file.read(name_l)

                        unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                        unzip_data = bsa_file.read(file_data[k].file_size)

                        try:
                            unzip_data = zlib.decompress(unzip_data)
                        except zlib.error:
                            bsa_file.seek(here)
                            unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                            unzip_data = bsa_file.read(file_data[k].file_size)

                            try:
                                unzip_data = zlib.decompress(unzip_data)
                            except zlib.error:
                                error = True

                    elif version == 105:  # Skyrim SE, Skyrim VR, Skyrim AE, Enderal SE
                        codec = ZipMethods.LZ4
                        here = bsa_file.tell()
                        fs = file_data[k].file_size
                        fi = file_data[k].file_info

                        if ext.lower() in ('dds', 'png', 'bmp') and fi != 64:
                            name_l = int.from_bytes(bsa_file.read(1))
                            file_name = bsa_file.read(name_l)

                        if fi != 64:
                            unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)

                        unzip_data = bsa_file.read(fs if fi in (0, 64) else unzip_size + fs)

                        try:

                            if fi != 64:
                                unzip_data = lz4.frame.decompress(unzip_data)

                        except RuntimeError:
                            a = 2

                            while True:
                                bsa_file.seek(here)
                                unzip_size = int.from_bytes(bsa_file.read(4), byteorder=byteorder)
                                unzip_data = bsa_file.read(fs * a)

                                try:
                                    unzip_data = lz4.frame.decompress(unzip_data)
                                    break
                                except RuntimeError:
                                    a += 1

                                if a == 100:
                                    error = True
                                    break

                else:
                    unzip_data = bsa_file.read(file_data[k].file_size)

                with open(path, 'wb') as new_file:
                    new_file.write(unzip_data)

                if compressed and error:
                    self.unzip(path, codec)

